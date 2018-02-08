import argparse
from base64 import b85decode
import logging
import json
from pathlib import Path
import sys

log_format = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)


class Config:
    def __init__(self):

        self.debug = False

        self.jd = {
            'username': '',
            'password': ''
        }

    @classmethod
    def load(cls, d):
        the_config = Config()

        the_config.debug = d.get('debug', False)

        try:
            the_config.jd = {
                'username': b85decode(d['jd']['username']).decode(),
                'password': b85decode(d['jd']['password']).decode()
            }
        except Exception as e:
            logging.error('获取京东帐号配置出错: ' + repr(e))

        return the_config


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name')
    args = parser.parse_args()

    config_name = args.config or 'config.json'
    logging.info('使用配置文件 "{}".'.format(config_name))

    config_file = Path(__file__).parent.joinpath('../conf/', config_name)

    if not config_file.exists():
        config_name = 'config.default.json'
        logging.warning('配置文件不存在, 使用默认配置文件 "{}".'.format(config_name))
        config_file = config_file.parent.joinpath(config_name)

    try:
        config_file = config_file.resolve()
        config_dict = json.loads(config_file.read_text())
    except Exception as e:
        sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

    the_config = Config.load(config_dict)

    return the_config


config = load_config()
