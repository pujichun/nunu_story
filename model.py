class StoryItem(object):
    def __init__(self, author="", book_name="", content="", url="", chapter="", callback=""):
        self.author = author
        self.book_name = book_name
        self.chapter = chapter
        self.content = content
        self.url = url
        self.callback = callback
        self.source = ""

    def __repr__(self):
        return f"StoryItem(author: {self.author}, book_name: {self.book_name}, chapter: {self.chapter}, content: {self.content}, callback: {self.callback}, url: {self.url})"


class LinkItem(object):
    def __init__(self, url="", callback=""):
        self.url = url
        self.callback = callback
        self.source = ""

    def __repr__(self):
        return f"LinkItem(url: {self.url}, callback: {self.callback})"


if __name__ == '__main__':
    s = StoryItem()
    print(s)
