import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import requests
import re

# 取排行榜第一列数据 在第几列
index_map = {
    'rzdf': 6,
    'zzf': 7,
    '1yzf': 8,
    '3yzf': 9,
    '6yzf': 10,
    '1nzf': 11,
}
#  接口参数映射为 普通字段
month_map = {
    'rzdf': 'dayGrowRate',
    'zzf': 'last1week',
    '1yzf': 'last1month',
    '3yzf': 'last3month',
    '6yzf': 'last6month',
    '1nzf': 'last1year'
}


async def parse_data(data, fund_type, month_type):
    pattern = r'rankData = {datas:(.*?),allRecords:'
    all_datas = re.search(pattern, data)
    if all_datas.group(1):
        datas = json.loads(all_datas.group(1))
        line = datas[0]
        # print(line)
        # 168401,红土转型精选混合(LOF),HTZXJXHHLOF,2022-08-22,3.1898,3.1898,0.07,3.47,9.92,31.55,13.92,1.16,83.32,154.61,1.69,218.98,2016-12-30,1,72.3007,1.50%,0.15%,1,0.15%,1,215.73
        index = index_map[month_type]
        d = {
            'name': line.split(',')[1],
            'code': line.split(',')[0],
            month_map[month_type]: line.split(',')[index],
            'date': line.split(',')[3],
            'type': fund_type,
        }
        # print(d)
        return d


async def get(fund_type, month_type):
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx'
    params = {
        'op': 'ph',
        'dt': 'kf',
        'ft': fund_type,  # 'ft': 'gp',zq zs qdii lof fof hh
        'rs': '',
        'gs': '0',
        'sc': month_type,  # rzdf zzf 1yzf 3yzf 6yzf 1nzf
        'st': 'desc',
        'sd': '2020-09-24',
        'ed': '2021-09-24',
        'qdii': '',
        'tabSubtype': ',,,,,',
        'pi': '1',
        'pn': '50',
        'dx': '1',
        'v': '0.31991931569189114',
    }
    headers = {
        # 'Cookie':'st_si=62531298629766; st_asi=delete; ASP.NET_SessionId=crzmplcpi3y4jo1zsqaq2ady; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; qgqp_b_id=ecf1889c4b76aee4597b3b17d5b3e10d; EMFUND0=null; EMFUND8=07-29%2019%3A01%3A13@%23%24%u4E2D%u5E9A%u4EF7%u503C%u9886%u822A%u6DF7%u5408@%23%24006551; EMFUND9=07-30 10:30:02@#$%u5E7F%u53D1%u9053%u743C%u65AF%u77F3%u6CB9%u6307%u6570%u4EBA%u6C11%u5E01A@%23%24162719; st_pvi=89169893311724; st_sp=2022-05-19%2023%3A42%3A57; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F162719.html; st_sn=10; st_psi=20220822021003589-112200312936-5604293987',
        # 'Host': 'fund.eastmoney.com',
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
    session = aiohttp.ClientSession()
    response = await session.get(url, headers=headers, params=params)
    # print(response.status, 111)
    data = await response.text()
    # if response.status == 200:
    datas = await parse_data(data, fund_type, month_type)
    await session.close()
    return datas
    # return None


async def request(date_type):
    types = ['gp', 'zq', 'zs', 'qdii', 'hh', 'fof']
    datas = []
    for fund_type in types:
        res = await get(fund_type=fund_type, month_type=date_type)
        datas.append(res)
    # print(res)

    for d in datas:
        if d['type'] == 'qdii' or d['type'] == 'fof':
            d['date'] = datas[0].get('date')
    # print(datas)

    return datas


def main():
    date_types = ['rzdf', 'zzf', '1yzf', '3yzf', '6yzf', '1nzf']

    tasks = [asyncio.ensure_future(request(i)) for i in date_types]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        # print(task, 111)
        print(task.result())


async def main2():
    # asyncio.gather 按顺序输出
    date_types = ['rzdf', 'zzf', '1yzf', '3yzf', '6yzf', '1nzf']

    tasks = [asyncio.ensure_future(request(i)) for i in date_types]
    res = await asyncio.gather(*tasks)
    return res


if __name__ == '__main__':
    # rzdf    zzf    1yzf   3yzf   6yzf  1nzf
    # 日增长率 近一周  近一月  近三月  近6月  近一年

    # # for date_type in date_types:
    # #     aggreate_data(date_type)
    #
    # aggreate_data('1yzf')
    # start = time.time()
    # loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(main2())
    # print(res)
    # print(time.time() - start)

    async def first_task():
        print("First Task")


    async def second_task():
        print("Second Task")


    async def third_task():
        print("Third Task")


    async def main():
        await asyncio.gather(first_task(), second_task(), third_task())


    asyncio.run(main())
