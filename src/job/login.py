from requests import Session

import browser
import job


class Login:
    job_name = '登录'

    index_url = 'https://bk.jd.com/m/channel/login/daka.html'
    login_url = 'https://home.m.jd.com'
    test_url = index_url

    logger = job.logger

    def __init__(self, session: Session):
        self.session = session
        self.job_success = False

    def run(self):
        self.logger.info('Job Start: {}'.format(self.job_name))

        is_login = self.is_login()
        self.logger.info('登录状态: {}'.format(is_login))

        if not is_login:
            self.logger.info('进行登录...')
            try:
                self.login()
                self.logger.info('登录成功')
            except Exception as e:
                self.logger.error('登录失败: {}'.format(repr(e)))

        if is_login:
            self.job_success = True

        self.logger.info('Job End.')

    def is_login(self):
        r = self.session.get(self.test_url, allow_redirects=False)

        if r.is_redirect and 'passport' in r.headers['Location']:
            return False
        else:
            return True

    def login(self):
        cookies = browser.get_cookies(self.login_url)
        self.session.cookies.update(cookies)
