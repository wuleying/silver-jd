import logging
import sys

logger = logging.getLogger('App.JD')
formatter = logging.Formatter('%(asctime)s %(name)s[%(module)-s] %(levelname)s: %(message)s')


def set_logger():
    logger.propagate = False
    logger.setLevel(logging.INFO)

    # 文件日志
    file_handler = logging.FileHandler("/tmp/silver-jd.log")
    file_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


set_logger()
