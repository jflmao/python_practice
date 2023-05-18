# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  51.py
# @Author  ：  jflmao
# @Time    ：  2023-05-18 15:22
# @Software：  PyCharm
# ==============================
import time
import requests

import execjs
from urllib import parse

with open('51sign.js') as f:
    jstext = f.read()
job = execjs.compile(jstext)
url = "https://cupidjob.51job.com/open/noauth/search-pc"
dirpath = '/open/noauth/search-pc'
params = {
    "api_key": "51job",
    "timestamp": str(int(time.time())),
    "keyword": "爬虫",  # 搜索关键字
    "searchType": "2",
    "function": "",
    "industry": "",
    "jobArea": "190200",  # 地区代码
    "jobArea2": "",
    "landmark": "",
    "metro": "",
    "salary": "",
    "workYear": "",
    "degree": "",
    "companyType": "",
    "companySize": "",
    "jobType": "",
    "issueDate": "",
    "sortType": "0",
    "pageNum": "1",  # 翻页
    "requestId": "",
    "pageSize": "20",  # 每页返回的数量
    "source": "1",
    "accountId": "",
    "pageCode": "sou|sou|soulb"
}
val = '{}?{}'.format(dirpath, parse.urlencode(params))
sign = job.call('get_sign', val)
uuid = job.call('get_uuid')

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Referer": "https://we.51job.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    "sign": sign,
    "uuid": uuid
}

cookies = {
    "guid": uuid,
    "nsearch": "jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D",
    "uid": "wKhJC2Q4Gq5BKUxOV/MhAg==",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%2256e004e4b5d67c823a49388630541569%22%2C%22first_id%22%3A%221877b283048ac1-0e034d0bba9c0f-7a545474-2073600-1877b283049981%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fappssry6rs71641.h5.xiaoeknow.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3N2IyODMwNDhhYzEtMGUwMzRkMGJiYTljMGYtN2E1NDU0NzQtMjA3MzYwMC0xODc3YjI4MzA0OTk4MSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjU2ZTAwNGU0YjVkNjdjODIzYTQ5Mzg4NjMwNTQxNTY5In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2256e004e4b5d67c823a49388630541569%22%7D%2C%22%24device_id%22%3A%221877b283048ac1-0e034d0bba9c0f-7a545474-2073600-1877b283049981%22%7D",
    "slife": "lastvisit%3D010000%26%7C%26",
    "JSESSIONID": "5444DAC3F2B51A3E860C0D5795C338FF",
    "acw_tc": "ac11000116843973762215847e00dfe10d5b532b97e24d907562c79d0340a3",
    "acw_sc__v2": "6465dd403a4a3e1ac8789a4c5a2889db6aa6dbd9",
    "search": "jobarea%7E%60190200%7C%21recentSearch0%7E%60190200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60010000%2C190200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21",
    "ssxmod_itna": "iu0QPfODCF0LxYKHe7uRDUxmu8syKC3fK9ADBd42xiNDnD8x7YDvC+ODG2xiKZzYn6Yq3hPAjgvfhSi6YbxWh3Sm5bDHxY=DUaAvw5D4fKGwD0eG+DD4DWDmeHDnxAQDjxGpc2LkX=DEDYpcDDoDY86RDitD4qDBzrdDKqGgFkG3nrvcQWdPETbg300Y+7=DjwbD/4xayn2aka5ZQCnbqepRDB=1xBQMAkNUmeDHCwXM4nvxiE5rBEv5iip4+0wxnherSoufdGGbEDAP3EvQ/I45tO41DDfYnO+0wiD=",
    "ssxmod_itna2": "iu0QPfODCF0LxYKHe7uRDUxmu8syKC3fK9D8MjDDKDOKDBLY8x7p4XSAjxUpc=0jPOi6GrFELb6Q0+nbErviwGGEuYS3zQd2LYcx=BK1oHDwCmjvTvj481LPFFS0jXH8MCKwbgL5Ip/d08RwiqHb0qLgjep8oL8R2uj8EGIeIV7m0x6l3xsjXZepu=1jE+beI+jSj4fEAuR4fubbQ7jZfmmky=M15Cc2HhL3Bj43y8PUECr/I=xApUKFtEPUGFG28kuzMAuR67lIg8GIF6uRSujKSH19lLGX1EmNF6h48MOVap6IlgMy24KD5Bgb+ci0DgagUcxubTbHH/yq1b=9Ped5P1AW9Y9+2Kk+lf9LIHi75PpygI5xHEMiHKwKOmFbY0ZGO4NA32Hr4OSCO3qw=uy=nKo=nihIaQErcPQH5B7RoD07nAq6AD7xFaBaO0PQxLGgolEP1a5YADOAPNokfoQw6jYD+M+KcAPHAUA=4Oa=90U9g=GgfF2UC1Doj64UUkpo5OHk7jPY=A1PMZ2BpQkB0ooUXf4F/oLYK6puPRRaAPD7=DY93eD="
}

response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
for item in response['resultbody']['job']['items']:
    print('公   司：', item['fullCompanyName'],
          '\n岗   位：', item['jobName'],
          '\n薪   酬：', item['provideSalaryString'],
          '\n工作经验：', item['jobTags'][0],
          '\n学历要求：', item['jobTags'][1],
          '\n====================================')
