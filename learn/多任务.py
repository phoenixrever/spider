# coding: utf-8

import asyncio
import time
import requests
import aiohttp
import os


async def request(url):
    print("正在请求。。。", url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }
    # 在异步协程中如果出现了同步模块相关的代码，那么就无法实现异步 time.sleep(2) 属于同步
    await asyncio.sleep(2)
    # 同理 requests.get 请求也是 需要使用异步网络模块aiohttp
    async with aiohttp.ClientSession() as session:
        # proxy: http://ip:port
        async with await session.get('https://www.baidu.com/',headers=headers) as response:
            # read() 返回二进制 json()
            text = await  response.text()
            with open('baidu.html','w',encoding='utf-8') as fp:
                fp.write(text)
            # print(text)
    print("请求结束", url)


urls = ["first", 'second', 'third', 'four', 'five']
stacks = []
if __name__ == '__main__':
    for url in urls:
        task = asyncio.ensure_future(request(url))
        stacks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(stacks))
