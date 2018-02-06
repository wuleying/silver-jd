import logging

logger = logging.getLogger('App.JD')
formatter = '%(asctime)s %(name)s[%(module)-s] %(levelname)s: %(message)s'

def set_logger():
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)


set_logger()
