from requests import Session

from .login import Login


class Buy(Login):
    job_name = '商品购买'

    def __init__(self, session: Session):
        super().__init__(session)
        self.page_data = ''

    def buy(self):
        return True
