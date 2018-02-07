import json
import re

import requests
from lxml import etree

import jd


class JD(object):
    logger = jd.logger

    # 请求URL
    passport_url = 'https://passport.jd.com/new/login.aspx'
    login_url = 'https://passport.jd.com/uc/loginService'
    cart_url = 'https://cart.jd.com/gate.action?pid={}&pcount={}&ptype=1'

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

    sel = ''
    request_session = ''

    track_id = ''
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
            self.sel = etree.HTML(request.content)

        self.auth_code = 'http:' + self.sel.xpath('//img[@id="JD_Verification1"]/@src2')[0]
        self.params = {
            'uuid': self.sel.xpath('//input[@id="uuid"]/@value')[0],
            'eid': self.sel.xpath('//input[@id="eid"]/@value')[0],
            '_t': self.sel.xpath('//input[@id="token"]/@value')[0],
            'loginType': 'c',
            'loginname': username,
            'nloginpwd': password,
            'pubKey': self.sel.xpath('//input[@id="pubKey"]/@value')[0],
            'sa_token': self.sel.xpath('//input[@id="sa_token"]/@value')[0],
            'chkRememberMe': '',
            'authcode': '',
        }

    # 登录
    def login(self):
        print(self.auth_code)

        if self.auth_code != '':
            # 手动输验证码
            self.params['authcode'] = input('Please input verification: ')

        login_request = self.request_session.post(self.login_url, data=self.params, headers=self.login_headers)
        patt = '<Cookie TrackID=(.*?) for .jd.com/>'
        self.track_id = re.compile(patt).findall(str(self.request_session.cookies))
        js = json.loads(login_request.text[1:-1])
        if js.get('success'):
            self.logger.info('Login success!')
        else:
            self.logger.error('Login failure!')
            exit(0)

    # 加购物车
    def cart(self):
        self.pid = input('Please input goods code:')
        self.count = input('Please input goods count:')

        cart_request = self.request_session.get(self.cart_url.format(self.pid, self.count))
        self.logger.info(self.cart_url.format(self.pid, self.count))

        if re.compile('<title>(.*?)</title>').findall(cart_request.text)[0] == '商品已成功加入购物车':
            self.logger.info('Add cart success!')
        else:
            self.logger.error('Add cart failure!')
            exit(0)

    # 提交订单
    def submit(self):
        return True
