from jd.jd import *
from config import config


def main():
    jd = JD(config.jd["username"], config.jd["password"])
    jd.login()
    jd.cart()
    jd.submit()


if __name__ == '__main__':
    main()
