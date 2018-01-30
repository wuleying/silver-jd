package jd

import (
	"github.com/go-clog/clog"
	"github.com/wuleying/silver-jd/util"
	"net/http"
	"net/url"
)

// 签到
func (jd *JingDong) VipSignIn() error {
	u, _ := url.Parse(util.URL_SIGN_IN)
	q := u.Query()
	q.Set("token", jd.token)
	u.RawQuery = q.Encode()

	req, err := http.NewRequest("GET", u.String(), nil)
	if err != nil {
		clog.Info("Sign in（%+v）failed: %+v", util.URL_SIGN_IN, err.Error())
		return err
	}

	resp, err := jd.client.Do(req)
	if err != nil {
		clog.Info("Sign in（%+v）failed: %+v", util.URL_SIGN_IN, err.Error())
		return err
	}

	if resp.StatusCode == http.StatusOK {
		clog.Info("Sign in（%+v) success.", util.URL_SIGN_IN)
	}

	return nil
}
