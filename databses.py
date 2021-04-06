import aiomysql
import asyncio


class MySQL:
    """
    单例模式，初始化完成对象之后一直使用初始化完成后的连接池
    """
    pool = None

    @classmethod
    async def init_pool(cls):
        try:
            if not cls.pool:
                __pool = await aiomysql.create_pool(
                    minsize=5,  # 连接池最小值
                    maxsize=20,  # 连接池最大值
                    host='127.0.0.1',
                    port=3306,
                    user='pujic',
                    password='a',
                    db='nunu_story',
                    autocommit=True,  # 自动提交模式
                )
                cls.pool = __pool
        except Exception as e:
            print(e)

    async def get_cursor(self):
        """
        从连接池中请求一个连接对象
        """
        conn = await self.pool.acquire()
        cursor = await conn.cursor(aiomysql.DictCursor)
        return conn, cursor

    async def execute(self, query, param=None):
        conn, cursor = await self.get_cursor()
        try:
            await cursor.execute(query, param)
            if cursor.rowcount == 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
        finally:
            if cursor:
                await cursor.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

    async def query(self, query, param=None):
        conn, cursor = await self.get_cursor()
        try:
            await cursor.execute(query, param)
            return await cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if cursor:
                await cursor.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)


async def test():
    mysql = MySQL()
    await mysql.init_pool()
    res = await mysql.query("SELECT * FROM author")
    print(res)


if __name__ == '__main__':
    asyncio.run(test())
