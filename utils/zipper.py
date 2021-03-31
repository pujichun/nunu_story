import bz2
import binascii
from utils import log


@log.log
def zipped(text: str) -> bytes:
    compressed = bz2.compress(text.encode("utf8"))
    res = binascii.hexlify(compressed)
    return res


@log.log
def unzip(text) -> str:
    unhex = binascii.unhexlify(text)
    res = bz2.decompress(unhex)
    return res.decode("utf8")


if __name__ == '__main__':
    e = zipped("你好！")
    print(e)
    print(unzip(e))
