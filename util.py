import bz2
import binascii


def zipped(text: str):
    """
    :param text: 字符串对象
    :return: 压缩后的数据
    """
    compressed = bz2.compress(text.encode("utf8"))
    res = binascii.hexlify(compressed)
    return res
