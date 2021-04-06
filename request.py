import aiohttp
import custem_queue
from hashlib import md5


async def request(session: aiohttp.ClientSession, url: str):
    # 将要爬取的URL放入集合去重
    custem_queue.USED_URL.add(md5(url.encode("utf8")).hexdigest())
    print(url)
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                html = await resp.text(encoding="gb2312", errors="ignore")
                return html
            print(resp.status)
            return None
    except Exception as e:
        print(e)
        return None
