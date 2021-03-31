from lxml import etree
from utils import log
from urllib.parse import urljoin
from model import LinkItem
import the_items


@log.log
def author_classification_parser(base_url: str, source: str):
    """解析首页的作家分类
    :return 返回作家分类页面链接
    """
    _element = etree.HTML(source)
    classification_urls = _element.xpath('//td[@height="30" and @align="center"]//a/@href')

    def foo(u):
        return urljoin(base_url, u)
    items = []
    for url in map(foo, classification_urls):

        if url[-13:] == "files/writer/":
            _item = LinkItem(url=url, callback="parses.authors_list_page.all_author_list_parser")
            items.append(_item)
        elif "/files/15.html" in url:
            _item = LinkItem(url=url, callback="parses.authors_list_page.korea_author_parser")
            items.append(_item)
        elif "author" in url:
            _item = LinkItem(url=url, callback="parses.authors_list_page.author_classification_list_parser")
            items.append(_item)
        else:
            print(f"error: {url}")
    the_items.update_item(items)
