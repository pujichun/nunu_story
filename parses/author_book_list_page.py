from lxml import etree
from utils import log
from urllib.parse import urljoin
from copy import deepcopy
from model import StoryItem
import the_items
from spider import fetch



@log.log
def author_book_list_page_parser(item: StoryItem):
    """parses author works
    :return: this author's book links
    """
    source = fetch(item.url)
    if source:
        _element = etree.HTML(source)
        element_a = _element.xpath('//td[@valign="top" and @bgcolor="#ffffff"]//a[@target="_blank"]')
        items = []
        for a in element_a:
            _item = deepcopy(item)
            try:
                book_name = a.xpath('./text()')
                if not book_name:
                    book_name = a.xpath('./font/text()')
                if not book_name:
                    book_name = a.xpath('./strong/text()')
                if not book_name:
                    book_name = a.xpath('./img/@alt')
                if not book_name:
                    book_name = a.xpath('./font/strong/text()')
                if not book_name:
                    book_name = a.xpath('./strong/font/text()')
                link = a.xpath('./@href')[0]
                _item.book_name = book_name[0]
                _item.url = urljoin(_item.url, link)
            except Exception as e:
                print(item.url, "这个作家没有书籍")
                continue
            _item.callback = "parses.chapter_page.chapter_parser"
            items.append(_item)
        the_items.update_item(items)
