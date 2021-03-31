from spider import fetch
import parses.home_page
import parses.author_book_list_page
import parses.content_page
import parses.authors_list_page
import parses.chapter_page
import the_items


def engine():
    # 请求首页获取作家分类链接
    source = fetch(the_items.HOST)
    if source:
        parses.home_page.author_classification_parser(the_items.HOST, source)
    else:
        print("error in host page")
    # 如果爬取队列中有item那么就一直执行
    while the_items.WAIT_FOR_USE_ITEMS:
        item = the_items.WAIT_FOR_USE_ITEMS.pop()
        callback = eval(item.callback)
        callback(item)
    print("END")


if __name__ == '__main__':
    engine()
