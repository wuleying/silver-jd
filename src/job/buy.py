import re

from requests import Session

from .login import Login


class Buy(Login):
    job_name = '商品购买'

    index_url = 'https://home.m.jd.com'
    add_cart_url = 'https://cart.jd.com/gate.action?pid=3315699&pcount=1&ptype=1'
    test_url = 'https://home.m.jd.com'

    def __init__(self, session: Session):
        super().__init__(session)
        self.page_data = ''

    def app_run(self):
        self.add_cart()
        return True

    def add_cart(self):
        response = self.session.get(self.add_cart_url)

        #self.logger.info(response.text)

        if re.compile('<title>(.*?)</title>').findall(response.text)[0] == '商品已成功加入购物车':
            self.logger.info('商品已成功加入购物车')
            return True
        else:
            self.logger.info('添加购物车失败')
            return False

    def buy(self):
        return True

