package util

import (
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
)
