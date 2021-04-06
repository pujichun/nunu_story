class Item:
    """
    数据模板
    """
    def __init__(self):
        self.url = ""
        self.author = ""
        self.book = ""
        self.chapter = ""
        self.content = ""
        self.callback = ""

    def __repr__(self):
        return f'Item(url:{self.url}, author:{self.author}, book: {self.book}, ' \
               f'chapter:{self.chapter}, content:{self.content}, ' \
               f'callback:{self.callback})'
