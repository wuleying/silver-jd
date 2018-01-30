package jd

import (
	"compress/gzip"
	"fmt"
	"github.com/go-clog/clog"
	"github.com/wuleying/silver-jd/util"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"
)

var (
	URLForQR = [...]string{
		"https://passport.jd.com/new/login.aspx",
		"https://qr.m.jd.com/show",
		"https://qr.m.jd.com/check",
		"https://passport.jd.com/uc/qrCodeTicketValidation",
		"http://home.jd.com/getUserVerifyRight.action",
	}

	DefaultHeaders = map[string]string{
		"User-Agent":      "Chrome/51.0.2704.103",
		"ContentType":     "application/json",
		"Connection":      "keep-alive",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.8",
	}

	maxNameLen   = 40
	cookieFile   = fmt.Sprintf("%s/%s", util.ROOT_DIR, "cookies/jd.cookies")
	qrCodeFile   = "cookies/jd.qr"
	strSeperater = strings.Repeat("+", 60)
)

// JDConfig ...
type JDConfig struct {
	Period     time.Duration // refresh period
	ShipArea   string        // shipping area
	AutoRush   bool          // continue rush when out of stock
	AutoSubmit bool          // whether submit the order
}

// SKUInfo ...
type SKUInfo struct {
	ID        string
	Price     string
	Count     int    // buying count
	State     string // stock state 33 : on sale, 34 : out of stock
	StateName string // "现货" / "无货"
	Name      string
	Link      string
}

// JingDong wrap jing dong operation
type JingDong struct {
	JDConfig
	client *http.Client
	jar    *util.SimpleJar
	token  string
}

func NewJingDong(option JDConfig) *JingDong {
	jd := &JingDong{
		JDConfig: option,
	}

	jd.jar = util.NewSimpleJar(util.JarOption{
		JarType:  util.JarGob,
		Filename: cookieFile,
	})

	if err := jd.jar.Load(); err != nil {
		clog.Error(0, "加载Cookies失败: %s", err)
		jd.jar.Clean()
	}

	jd.client = &http.Client{
		Timeout: time.Minute,
		Jar:     jd.jar,
	}

	return jd
}

func (jd *JingDong) Release() {
	if jd.jar != nil {
		if err := jd.jar.Persist(); err != nil {
			log.Panic("Failed to persist cookiejar. error %+v.", err)
		}
	}
}

func (jd *JingDong) getResponse(method, URL string, queryFun func(URL string) string) ([]byte, error) {
	var (
		err  error
		req  *http.Request
		resp *http.Response
	)

	queryURL := URL
	if queryFun != nil {
		queryURL = queryFun(URL)
	}

	if req, err = http.NewRequest(method, queryURL, nil); err != nil {
		return nil, err
	}
	applyCustomHeader(req, DefaultHeaders)

	if resp, err = jd.client.Do(req); err != nil {
		return nil, err
	}

	defer resp.Body.Close()
	var reader io.Reader

	switch resp.Header.Get("Content-Encoding") {
	case "gzip":
		reader, _ = gzip.NewReader(resp.Body)
	default:
		reader = resp.Body
	}

	return ioutil.ReadAll(reader)
}
