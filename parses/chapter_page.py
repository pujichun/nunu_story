from lxml import etree
from spider import fetch
from utils import log
from urllib.parse import urljoin
from model import StoryItem
from copy import deepcopy
import the_items


@log.log
def chapter_parser(item: StoryItem):
    """parses book page
    :return this book's chapter links
    """
    source = fetch(item.url)
    if source:
        _element = etree.HTML(source)
        element_a = _element.xpath('//tr[@bgcolor="#ffffff"]/td/a')
        items = []
        for a in element_a:
            _item = deepcopy(item)
            chapter = a.xpath('./text()')[0]
            link = a.xpath('./@href')[0]
            _item.chapter = chapter
            _item.url = urljoin(_item.url, link)
            _item.callback = "parses.content_page.text_parser"
            items.append(_item)
        the_items.update_item(items)
