from hashlib import md5
from typing import List
from collections import deque

from modle import Item

WAIT_FOR_USE_ITEM = deque()
USED_URL = set()


async def update(items: List[Item]):
    for item in items:
        if (md5(item.url.encode("utf8")).hexdigest() not in USED_URL) and ("https://www.kanunu8.com/" in item.url):
            WAIT_FOR_USE_ITEM.append(item)
