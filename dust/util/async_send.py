#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/24 18:48

import asyncio
import aiohttp
import time,datetime

start_time = time.time()

async def requests(method,url,data,cookies):
    async with aiohttp.request(method.upper(),url,data=data,cookies=cookies) as response:
        result = await response.text()
        response.close()
        return result

async def request(method,index,url,data,cookies):
    result = await requests(method,url,data,cookies)
    # print('POST response from', url, 'Result:', result,"num:",index+1)
    return {'url':url,'result':result,'index':index}

def main(url,data,token,method):
    # try:
        result = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(request(method=method,index=index,
                                               url=url,data=data,cookies=value))
                 for index,value in enumerate(token)]

        loop = asyncio.get_event_loop()
        info = loop.run_until_complete(asyncio.wait(tasks))
        end_time = time.time()
        use_time = end_time - start_time
        for i in info[0]:
            result.append(i.result())
        result.append({'user_time':use_time})
        return result
    # except Exception as e:
    #     return {0:e}

if __name__ == '__main__':
    url = 'https://www.baidu.com'
    method = 'GET'
    token = [{} for _ in range(5)]
    data = {}
    info = main(url,data,token,method)
    print(info)
