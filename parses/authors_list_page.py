from lxml import etree
from utils import log
from urllib.parse import urljoin
from model import StoryItem, LinkItem
import the_items
from spider import fetch



@log.log
def all_author_list_parser(item: LinkItem):
    """解析所有作家页面的作家列表页
    :return 作家主页链接和下一页的链接
    """
    source = fetch(item.url)
    if source:
        _element = etree.HTML(source)
        element_a = _element.xpath('//tr[@align="middle"]/td//a')
        items = []
        for a in element_a:
            author = a.xpath('./text()')[0]
            print(author)
            link = a.xpath('./@href')[0]
            link = urljoin(item.url, link)
            if '18-' in link and link[-4:] == 'html':
                # 翻页
                _item = LinkItem(url=link, callback="parses.authors_list_page.all_author_list_parser")
                items.append(_item)

            elif "/files/writer/" in link or "/zj/" in link:
                _item = StoryItem(author=author, url=link,
                                  callback="parses.author_book_list_page.author_book_list_page_parser")
                items.append(_item)
            else:
                print(link)
        the_items.update_item(items)


@log.log
def author_classification_list_parser(item: LinkItem):
    """解析分类作家页面的作家列表页
    :return 作家主页链接
    """
    source = fetch(item.url)
    if source:
        _element = etree.HTML(source)

        element_a = _element.xpath('//td[@class="tb"]/p/a')
        items = []
        for a in element_a:
            author = a.xpath('./text()')[0]
            link = a.xpath('./@href')[0]
            link = urljoin(item.url, link)
            _item = StoryItem(author=author, url=link, callback="parses.author_book_list_page.author_book_list_page_parser")
            items.append(_item)
        the_items.update_item(items)


@log.log
def korea_author_parser(item: LinkItem):
    """ 解析韩国作家列表页
    :return: 作家主页链接
    """
    source = fetch(item.url)
    if source:
        _element = etree.HTML(source)
        element_a = _element.xpath('//td[@class="p12"]//a')
        items = []
        for a in element_a:
            author = a.xpath('./text()')[0]
            print(author)
            link = a.xpath('./@href')[0]
            link = urljoin(item.url, link)
            _item = StoryItem(author=author, url=link, callback="parses.author_book_list_page.author_book_list_page_parser")
            items.append(_item)
        the_items.update_item(items)
