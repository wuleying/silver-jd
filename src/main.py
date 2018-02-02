import logging
import os
import pickle
import traceback
from pathlib import Path
import requests

from config import config

def main():
    session = make_session()

def make_session() -> requests.Session:
    session = requests.Session()

    session.headers.update({
        'User-Agent': config.ua
    })

    data_file = Path(__file__).parent.joinpath('../data/cookies')

    if data_file.exists():
        try:
            bytes = data_file.read_bytes()
            cookies = pickle.loads(bytes)
            session.cookies = cookies
            logging.info('# 从文件加载 cookies 成功.')
        except Exception as e:
            logging.info('# 未能成功载入 cookies, 从头开始~')

    return session