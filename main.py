import aiohttp
import asyncio
from modle import Item
import parses
import custem_queue
import databses


async def engine():
    """
    协程爬虫引擎
    """
    mysql = databses.MySQL()
    await mysql.init_pool()
    async with aiohttp.TCPConnector(
            limit=20,
            force_close=True,
            enable_cleanup_closed=True,
    ) as tc:
        async with aiohttp.ClientSession(connector=tc) as session:
            # 初始化首页请求
            home_item = Item()
            home_item.url = "https://www.kanunu8.com/"
            await parses.home_page(session, home_item)
            # 如果任务总数大于等于20个那么一次就并发20个请求
            while True:
                if len(custem_queue.WAIT_FOR_USE_ITEM) == 0:
                    await asyncio.sleep(20)
                    if len(custem_queue.WAIT_FOR_USE_ITEM) == 0:
                        break
                tasks, i = [], 1
                if len(custem_queue.WAIT_FOR_USE_ITEM) >= 20:
                    i = 20
                for i in range(i):
                    item = custem_queue.WAIT_FOR_USE_ITEM.pop()
                    callback = eval(item.callback)
                    tasks.append(asyncio.ensure_future(callback(session, item)))
                # 等待任务队列中的任务完成
                await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(engine())
