package jd

import (
	"compress/gzip"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"github.com/go-clog/clog"
	"github.com/wuleying/silver-jd/util"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
)

type Account struct {
	Username string
	Password string
}

// PC端登录
func (account *Account) LoginPC() error {
	var (
		err      error
		request  *http.Request
		response *http.Response
		doc      *goquery.Document
	)

	client := &http.Client{}

	url, _ := url.Parse(util.URL_LOGIN)
	query := url.Query()
	url.RawQuery = query.Encode()

	clog.Trace("url=%s", url.String())

	if request, err = http.NewRequest("GET", url.String(), nil); err != nil {
		clog.Error(util.CLOG_SKIP_DEFAULT, "请求（%+v）失败: %+v", url.String(), err)
		return err
	}

	setHeaders(request)

	if response, err = client.Do(request); err != nil {
		clog.Error(util.CLOG_SKIP_DEFAULT, "请求（%+v）失败: %+v", url.String(), err)
		return err
	}

	if response.StatusCode != http.StatusOK {
		clog.Error(util.CLOG_SKIP_DEFAULT, "http status : %d/%s", response.StatusCode, response.Status)
	}

	defer response.Body.Close()

	// 获取返回的UUID
	if doc, err = goquery.NewDocumentFromReader(response.Body); err != nil {
		clog.Error(util.CLOG_SKIP_DEFAULT, "分析登录页面错误: %+v.", err)
		return err
	}

	uuid, isExist := doc.Find("#uuid").Attr("value")
	if isExist == false || len(uuid) < 1 {
		clog.Error(util.CLOG_SKIP_DEFAULT, "分析登录页面错误: uuid.")
		return err
	}

	token, isExist := doc.Find("#token").Attr("value")
	if isExist == false || len(token) < 1 {
		clog.Error(util.CLOG_SKIP_DEFAULT, "分析登录页面错误: token.")
		return err
	}

	pubKey, isExist := doc.Find("#pubKey").Attr("value")
	if isExist == false || len(pubKey) < 1 {
		clog.Error(util.CLOG_SKIP_DEFAULT, "分析登录页面错误: pubKey.")
		return err
	}

	saToken, isExist := doc.Find("#sa_token").Attr("value")
	if isExist == false || len(saToken) < 1 {
		clog.Error(util.CLOG_SKIP_DEFAULT, "分析登录页面错误: saToken.")
		return err
	}

	// 验证码
	authcode := ""

	login_service_url := fmt.Sprintf(util.URL_LOGIN_SERVICE, uuid, "http://jd.com", "0.6866403083063548", "2015")

	clog.Trace("login_service_url=%s", login_service_url)

	data, err := getResponse("POST", login_service_url, func(URL string) string {
		// 登录数据
		queryString := map[string]string{
			"uuid":          uuid,
			"_t":            token,
			"loginType":     "c",
			"loginname":     account.Username,
			"nloginpwd":     account.Password,
			"chkRememberMe": "",
			"authcode":      authcode,
			"pubKey":        pubKey,
			"sa_token":      saToken,
			"seqSid":        "9",
		}

		u, _ := url.Parse(login_service_url)
		q := u.Query()
		for k, v := range queryString {
			q.Set(k, v)
		}
		u.RawQuery = q.Encode()
		return u.String()
	})

	if err != nil {
		clog.Error(util.CLOG_SKIP_DEFAULT, "登录失败: %+v", err)
		return err
	}

	clog.Info(string(data))

	return nil
}

// 设置header
func setHeaders(request *http.Request) {
	if request == nil {
		return
	}

	for key, val := range util.HEADERS_DEFAULT {
		request.Header.Set(key, val)
	}
}

func getResponse(method, URL string, queryFun func(URL string) string) ([]byte, error) {
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
	setHeaders(req)

	client := &http.Client{}

	if resp, err = client.Do(req); err != nil {
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
