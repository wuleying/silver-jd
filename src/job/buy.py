from requests import Session

from .login import Login


class Buy(Login):
    job_name = '商品购买'

    # 加入购物车
    add_cart_url = 'https://cart.jd.com/gate.action?pid=%s&pcount=%s&ptype=1'

    def __init__(self, session: Session):
        super().__init__(session)
        self.page_data = ''

    def buy(self):
        self.add_cart()

        return True

    def add_cart(self):
        r = self.session.get(self.test_url, allow_redirects=False)
        return True
