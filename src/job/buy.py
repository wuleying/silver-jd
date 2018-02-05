import re
from . import common

from requests import Session

from .login import Login


class Buy(Login):
    job_name = '商品购买'

    # 加入购物车
    add_cart_url = 'https://cart.jd.com/gate.action?pid=3315699&pcount=1&ptype=1'

    def __init__(self, session: Session):
        super().__init__(session)
        self.page_data = ''

    def app_run(self):
        self.add_cart()
        self.buy()

        return True

    def buy(self):
        return True

    def add_cart(self):
        token = self._get_token()
        payload = {'token': token}

        response = self.session.get(self.add_cart_url, params=payload, allow_redirects=False)

        self.logger.info(self.add_cart_url)

        if re.compile('<title>(.*?)</title>').findall(response.text)[0] == '商品已成功加入购物车':
            self.logger.info('商品已成功加入购物车')
        else:
            self.logger.info('添加购物车失败')

        return True

    def _get_token(self):
        html = self._get_page_data()
        pattern = r'token:\s*"(\d+)"'
        token = common.find_value(pattern, html)

        if not token:
            raise Exception('token 未找到.')

        return token

    def _get_page_data(self):
        if not self.page_data:
            self.page_data = self.session.get(self.index_url).text

        return self.page_data
