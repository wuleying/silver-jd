import json
import re
import random

import requests
from lxml import etree

url = 'https://passport.jd.com/new/login.aspx'

passport_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'ContentType': 'text/html; charset=utf-8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
}

login_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Referer': 'https://passport.jd.com/uc/login?type=logout',
    'X-Requested-With': 'XMLHttpRequest'
}

request_session = requests.Session()
request_session.headers = passport_headers

# 请求登录页面
request = request_session.get(url=url, headers=passport_headers)
sel = etree.HTML(request.content)

uuid = sel.xpath('//input[@id="uuid"]/@value')[0]
eid = sel.xpath('//input[@id="eid"]/@value')[0]
t = sel.xpath('//input[@id="token"]/@value')[0]
pub_key = sel.xpath('//input[@id="pubKey"]/@value')[0]
sa_token = sel.xpath('//input[@id="sa_token"]/@value')[0]

verification = 'http:' + sel.xpath('//img[@id="JD_Verification1"]/@src2')[0]

random_num = random.random()
login_url = 'https://passport.jd.com/uc/loginService'


class JD(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.track_id = ''
        self.pid = ''

    def login(self):
        params = {
            'uuid': uuid,
            'eid': eid,
            '_t': t,
            'loginType': 'c',
            'loginname': self.username,
            'nloginpwd': self.password,
            'chkRememberMe': '',
            'authcode': '',
            'pubKey': pub_key,
            'sa_token': sa_token,
        }

        print(verification)

        if verification != '':
            # 手动输验证码
            params['authcode'] = input('Please input verification: ')

        req2 = request_session.post(login_url, data=params, headers=login_headers)
        patt = '<Cookie TrackID=(.*?) for .jd.com/>'
        self.track_id = re.compile(patt).findall(str(request_session.cookies))
        js = json.loads(req2.text[1:-1])
        if js.get('success'):
            print('Success!')
        else:
            print('failure!')

        return True
