package util

import (
	"fmt"
	"strings"
	"time"
)

// 全局常量
const (
	URL_SKU_STATE    = "https://c0.3.cn/stocks"
	URL_GOODS_DETS   = "http://item.jd.com/%s.html"
	URL_GOODS_PRICE  = "http://p.3.cn/prices/mgets"
	URL_ADD_TO_CART  = "https://cart.jd.com/gate.action"
	URL_CHANGE_COUNT = "http://cart.jd.com/changeNum.action"
	URL_CART_INFO    = "https://cart.jd.com/cart.action"
	URL_ORDER_INFO   = "http://trade.jd.com/shopping/order/getOrderInfo.action"
	URL_SUBMIT_ORDER = "http://trade.jd.com/shopping/order/submitOrder.action"
	URL_SIGN_IN      = "https://vip.jd.com/common/signin.html"
)

// 全局变量
var (
	// 根目录
	ROOT_DIR = FileGetParentDirectory(FileGetCurrentDirectory())
	// 当前时间
	CURRENT_TIME = time.Now().String()

	URL_FOR_QR = [...]string{
		"https://passport.jd.com/new/login.aspx",
		"https://qr.m.jd.com/show",
		"https://qr.m.jd.com/check",
		"https://passport.jd.com/uc/qrCodeTicketValidation",
		"http://home.jd.com/getUserVerifyRight.action",
	}

	DEFAULT_HEADERS = map[string]string{
		"User-Agent":      "Chrome/51.0.2704.103",
		"ContentType":     "application/json",
		"Connection":      "keep-alive",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.8",
	}

	MAX_NAME_LENGTH  = 40
	COOKIE_FILE      = fmt.Sprintf("%s/%s", ROOT_DIR, "cookies/jd.cookies")
	QR_CODE_FILE     = "cookies/jd.qr"
	STRING_SEPERATER = strings.Repeat("+", 60)
)
