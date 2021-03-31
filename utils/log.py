import logging
import functools


def get_logger():
    """create logger"""
    logger = logging.getLogger()
    fmt = logging.Formatter("%(asctime)s-%(filename)s-[line:%(lineno)d]-%(levelname)s:%(message)s")
    fh = logging.FileHandler("log")
    sh = logging.StreamHandler()
    fh.setFormatter(fmt)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel("INFO")
    return logger


_logger = get_logger()


def log(f):
    """log decorator"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        _logger.info(f"正在执行{f.__name__}函数")
        res = f(*args, **kwargs)
        return res

    return wrapper
