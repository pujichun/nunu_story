from lxml import etree
from urllib.parse import urljoin
from modle import Item
from request import request
import custem_queue
from copy import deepcopy
from util import zipped
import databses


async def home_page(session, item: Item):
    """
    解析首页，将作家分类页面的信息爬取解析后放入总任务队列
    :param session: http会话对象
    :param item: Item对象
    """
    html = await request(session=session, url=item.url)
    if html:
        _element = etree.HTML(html)
        res = _element.xpath('//td[@height="30" and @align="center"]//a/@href')[1:]
        items = []
        for link in res:
            _item = Item()
            _item.url = urljoin(item.url, link)
            _item.callback = "parses.author_list"
            items.append(_item)
        await custem_queue.update(items)


async def author_list(session, item: Item):
    """
    解析作家分类列表页，将作家信息解析后放入总任务队列
    :param session: http会话对象
    :param item: Item对象
    """
    html = await request(session=session, url=item.url)
    if html:
        _element = etree.HTML(html)
        xpath_expression = '//td[@class="tb"]/p/a'
        if "/files/15.html" in item.url:
            xpath_expression = '//td[@class="p12"]//a'
        tags = _element.xpath(xpath_expression)
        items = []
        for tag in tags:
            _item = Item()
            _item.author = tag.xpath("./text()")[0]
            _item.url = urljoin(item.url, tag.xpath("./@href")[0])
            _item.callback = 'parses.book_list'
            items.append(_item)
        await custem_queue.update(items)


async def book_list(session, item: Item):
    """
    解析书籍列表页，将书籍信息解析后放入总任务队列
    :param session: http会话对象
    :param item: Item对象
    """
    html = await request(session=session, url=item.url)
    if html:
        _element = etree.HTML(html)
        tags = _element.xpath('//td[@valign="top" and @bgcolor="#ffffff"]//a[@target="_blank"]')
        items = []
        for tag in tags:
            # 使用深拷贝复制作家信息
            _item = deepcopy(item)
            try:
                # 因为书籍的信息有多种，因此尝试多种解析方式
                book = tag.xpath('./text()')
                if not book:
                    book = tag.xpath("./font/text()")
                if not book:
                    book = tag.xpath('./strong/text()')
                if not book:
                    book = tag.xpath('./img/@alt')
                if not book:
                    book = tag.xpath('./font/strong/text()')
                if not book:
                    book = tag.xpath('./strong/font/text()')
                _item.book = book[0]
                _item.url = urljoin(_item.url, tag.xpath('@href')[0])
                _item.callback = 'parses.chapter_list'
                items.append(_item)
                # print(_item)
            except Exception as e:
                print(e)
                continue
        await custem_queue.update(items)


async def chapter_list(session, item: Item):
    """
    解析章节列表页，将解析到的章节信息放入总任务队列
    :param session: http会话对象
    :param item: Item对象
    """
    html = await request(session=session, url=item.url)
    if html:
        _element = etree.HTML(html)
        tags = _element.xpath('//tr[@bgcolor="#ffffff"]/td/a')
        items = []
        for tag in tags:
            _item = deepcopy(item)
            chapter = tag.xpath('./text()')[0]
            _item.chapter = chapter
            _item.url = urljoin(_item.url, tag.xpath('./@href')[0])
            _item.callback = "parses.content_text"
            items.append(_item)
        await custem_queue.update(items)


async def content_text(session, item: Item):
    """
    解析内容页面，将解析到的内容信息存入数据库
    :param session: http会话对象
    :param item: Item对象
    """
    html = await request(session=session, url=item.url)
    if html:
        _element = etree.HTML(html)
        text = "".join(_element.xpath('//p/text()'))
        if text:
            print("爬取到章节内容")
            item.content = zipped(text)
            mysql = databses.MySQL()
            await mysql.init_pool()
            await mysql.execute(f"call save_story_message(%s,%s,%s,%s)",
                                (item.author, item.book, item.chapter, item.content))
