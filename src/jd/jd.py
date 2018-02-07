import json
import re

import requests
from lxml import etree

import jd


class JD(object):
    logger = jd.logger

    passport_url = 'https://passport.jd.com/new/login.aspx'
    login_url = 'https://passport.jd.com/uc/loginService'

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

    track_id = ''
    pid = ''
    sel = ''

    request_session = ''

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
            self.logger.info('Login failure!')

        return True

    # 加购物车
    def cart(self):
        return True

    # 提交订单
    def submit(self):
        return True
