from lxml import etree
from spider import fetch
from utils import log
from model import StoryItem
import database
from utils import zipper

@log.log
def text_parser(item: StoryItem):
    """parses the book's chapter content
    :return this book's chapter content
    """
    source = fetch(item.url)
    if source:
        _element = etree.HTML(source)
        content = "".join(_element.xpath('//p/text()'))
        item.content = zipper.zipped(content)
        database.save_to_mysql(item=item)