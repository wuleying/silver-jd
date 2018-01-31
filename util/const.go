package util

import (
	"time"
)

// 全局常量
const (
	// URL地址
	URL_LOGIN = "http://passport.jd.com/new/login.aspx"

	// 权限
	FILE_READ_MODE  = 0644
	FILE_WRITE_MODE = 0666
	DIR_READ_MODE   = 0755
	DIR_WRITE_MODE  = 0777

	// clog skip级别
	CLOG_SKIP_DEFAULT      = 0
	CLOG_SKIP_DISPLAY_INFO = 2
)

// 全局变量
var (
	// 根目录
	ROOT_DIR = FileGetParentDirectory(FileGetCurrentDirectory())
	// 当前时间
	CURRENT_TIME = time.Now().String()

	HEADERS_DEFAULT = map[string]string{
		"User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
		"ContentType":     "text/html; charset=utf-8",
		"Connection":      "keep-alive",
		"Accept-Encoding": "deflate",
		"Accept-Language": "zh-CN,zh;q=0.8",
	}
)
