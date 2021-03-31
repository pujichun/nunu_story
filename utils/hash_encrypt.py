import hashlib
from utils import log


def md5(string: str) -> str:
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()
