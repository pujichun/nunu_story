import requests
from chardet.universaldetector import UniversalDetector
from requests.exceptions import RequestException
from utils import log
import html
import the_items
from utils import hash_encrypt


@log.log
def fetch(url) -> str:
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            detector = UniversalDetector()
            for line in response.iter_lines(1024):
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            encoding = detector.result['encoding']
            source = response.content.decode(encoding=encoding, errors="ignore")
            the_items.USED_URL.add(hash_encrypt.md5(url))
            return html.unescape(source)
        print(response.status_code)
        return ""
    except RequestException as e:
        print(e)
        return ""


if __name__ == '__main__':
    fetch("http://www.baidu.com/")
