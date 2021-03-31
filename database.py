import pymysql
from dbutils.pooled_db import PooledDB
from model import StoryItem
from utils import log
import functools


class MySQLPool(object):
    config = {
        "creator": pymysql,
        "host": "127.0.0.1",
        "port": 3306,
        "user": "pujic",
        "password": "a",
        "db": "nunu_story",
        "charset": "utf8",
        "mincached": 5,
        "maxcached": 8,
        # "blocking": True,
        "maxconnections": 50,
        'cursorclass': pymysql.cursors.DictCursor
    }
    pool = PooledDB(**config)

    def __enter__(self):
        self.conn = MySQLPool.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


def db_conn(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        with MySQLPool() as db:
            result = func(*args, db=db, **kw)
        return result

    return wrapper


@log.log
@db_conn
def test(db):
    try:
        db.cursor.execute("SELECT VERSION()")
        db.conn.commit()
        print(db.cursor.fetchone())
    except Exception as e:
        print(e)
        db.conn.rollback()


@log.log
@db_conn
def save_to_mysql(db, item: StoryItem):
    try:
        db.cursor.callproc("save_story_message", (item.author, item.book_name, item.chapter, item.content))
        db.conn.commit()
        print(f"成功写入{item}")
    except Exception as e:
        print(f"写入失败 {e}")
        db.conn.rollback()


if __name__ == "__main__":
    # mysql = MySQL()
    # conn = mysql.conn
    # cursor = conn.cursor()
    # cursor.
    #  print(cursor.fetchone())
    test()
