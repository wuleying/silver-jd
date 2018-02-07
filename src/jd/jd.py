import json
import random
import re
import time

import requests
from lxml import etree

import jd


class JD(object):
    logger = jd.logger

    # 请求URL
    # 通行证
    passport_url = 'https://passport.jd.com/new/login.aspx'
    # 账户登录
    login_url = 'https://passport.jd.com/uc/loginService'
    # 添加到购物车
    add_cart_url = 'https://cart.jd.com/gate.action?pid={}&pcount={}&ptype=1'
    # 购物车
    cart_url = 'https://cart.jd.com'
    # 取消商品
    cancel_item_url = 'https://cart.jd.com/cancelItem.action?rd={}'
    # 选择商品
    select_item_url = 'https://cart.jd.com/selectItem.action?rd={}'
    # 订单结算信息
    order_info_url = 'https://trade.jd.com/shopping/order/getOrderInfo.action?rid={}'
    # 提交订单
    submit_order_url = 'https://trade.jd.com/shopping/order/submitOrder.action'
    # stock
    stock_url = 'http://c0.3.cn/stock?skuId={}&cat=652,829,854&area={}'

    passport_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'ContentType': 'text/html; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }

    # 登录headers
    login_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Referer': 'https://passport.jd.com/uc/login?type=logout',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 地址编码
    area_code = '1_72_2799_0'
    # 下单重试时间，单位：秒
    sleep_time = 60

    request_session = ''

    track_id = ''
    e_id = ''
    # 商品ID
    pid = ''
    # 商品数量
    count = ''

    # 初始化
    def __init__(self, username, password):
        if self.request_session == '':
            self.request_session = requests.Session()
            self.request_session.headers = self.passport_headers

        # 请求登录页面
        request = self.request_session.get(url=self.passport_url, headers=self.passport_headers)
        sel = etree.HTML(request.content)

        self.e_id = sel.xpath('//input[@id="eid"]/@value')[0]
        self.auth_code = 'http:' + sel.xpath('//img[@id="JD_Verification1"]/@src2')[0]

        self.params = {
            'uuid': sel.xpath('//input[@id="uuid"]/@value')[0],
            'eid': self.e_id,
            '_t': sel.xpath('//input[@id="token"]/@value')[0],
            'loginType': 'c',
            'loginname': username,
            'nloginpwd': password,
            'pubKey': sel.xpath('//input[@id="pubKey"]/@value')[0],
            'sa_token': sel.xpath('//input[@id="sa_token"]/@value')[0],
            'chkRememberMe': '',
            'authcode': '',
        }

    # 登录
    def login(self):
        print(self.auth_code)

        if self.auth_code != '':
            # 手动输验证码
            self.params['authcode'] = input('Please input verification: ')

        request_login = self.request_session.post(self.login_url, data=self.params, headers=self.login_headers)
        patt = '<Cookie TrackID=(.*?) for .jd.com/>'
        self.track_id = re.compile(patt).findall(str(self.request_session.cookies))
        js = json.loads(request_login.text[1:-1])
        if js.get('success'):
            self.logger.info('Login success!')
        else:
            self.logger.error('Login failure!')
            exit(0)

    # 加购物车
    def cart(self):
        self.pid = input('Please input goods code:')
        self.count = input('Please input goods count:')

        request_add_cart = self.request_session.get(self.add_cart_url.format(self.pid, self.count))

        if re.compile('<title>(.*?)</title>').findall(request_add_cart.text)[0] == '商品已成功加入购物车':
            self.logger.info('Add cart success!')
        else:
            self.logger.error('Add cart failure!')
            exit(0)

    # 提交订单
    def submit(self):
        self.logger.info('开始尝试下单！')

        # 随机数
        r = random.random()

        item_data = {
            'outSkus': '',
            'pid': self.pid,
            'ptype': '1',
            'packId': '0',
            'targetId': '0',
            'promoID': '0',
            'locationId': '1-2810-6501-0'
        }

        # 取消商品
        self.request_session.post(self.cancel_item_url.format(str(r)), data=item_data)

        # 勾选商品
        self.request_session.post(self.select_item_url.format(str(r)), data=item_data)

        submit_data = {
            'overseaPurchaseCookies': '',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': self.track_id[0],
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'submitOrderParam.eid': self.e_id,
            'submitOrderParam.fp': 'b31fc738113fbc4ea5fed9fc9811acc6',
        }

        while True:
            request_stock = self.request_session.get(self.stock_url.format(self.pid, self.area_code))
            js = json.loads(request_stock.text)

            self.logger.info(js['stock']['StockState'])

            # 33有货 34无货
            if js['stock']['StockState'] == 33:
                self.logger.info('库存状态：有货')
                request_submit = self.request_session.post(self.submit_order_url, data=submit_data)
                self.logger.info('正在提交订单...')
                submit_js = json.loads(request_submit.text)

                # 判断是否下单成功
                if submit_js['success']:
                    self.logger.info('下单成功! 请速去付款！')
                    break
                else:
                    self.logger.info('下单失败! {}秒后重试。'.format(self.sleep_time))
                    # 重新尝试下单
                    time.sleep(self.sleep_time)
                    continue
            elif js['stock']['StockState'] != 33:
                self.logger.info('无货，{}秒后重试。'.format(self.sleep_time))
                time.sleep(self.sleep_time)
                continue
