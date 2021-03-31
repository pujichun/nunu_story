from utils import log

from utils import hash_encrypt

USED_URL = set()
WAIT_FOR_USE_ITEMS = set()

HOST = "https://www.kanunu8.com/"


def add_item(item):
    encrypt_url = hash_encrypt.md5(item.url)
    if encrypt_url not in USED_URL:
        WAIT_FOR_USE_ITEMS.add(item)


@log.log
def update_item(items):
    if isinstance(items, list):
        for item in items:
            add_item(item)
    else:
        add_item(items)
