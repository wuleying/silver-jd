package jd

import (
	"github.com/PuerkitoBio/goquery"
	"github.com/go-clog/clog"
	"github.com/wuleying/silver-jd/util"
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

	if isExist == false {
		clog.Error(util.CLOG_SKIP_DEFAULT, "分析登录页面错误: %+v.", err)
		return err
	}

	clog.Info("%s", uuid)

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
