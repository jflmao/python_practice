# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  获取淘宝数据信息.py
# @Author  ：  jflmao
# @Time    ：  2023-02-02 13:34
# @Software：  PyCharm
# ==============================
"""
    网址：https://s.taobao.com/search?initiative_id=staobaoz_20230111&q=Python
    需求：获取到20页数据，获取到'标题', '价格', '购买人数', '地点', '网址', '图片地址', '评论数', '店铺'
"""
import asyncio
import json
import re
import time

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient


class TaoBao:
    def __init__(self, _page):
        """
            初始化

        :param _page: 获取的页数
        """
        self.num = 0
        self.page = _page
        self.url = 'https://s.taobao.com/search?initiative_id=staobaoz_20230111&q=Python&s={}'
        self.headers = {
            "authority": "s.taobao.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Microsoft Edge\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"
        }
        self.cookies = {
            "_samesite_flag_": "true",
            "cookie2": "1ad64ad4716197895de88425ab9d452f",
            "t": "6103c9ecf564436e40dad27f9567dd43",
            "sgcookie": "E100myKwaO0hmDDtFkSR84orE5YxIR6y6q%2BeZcD4jx50rjviyGsFUvgURFGzidw2fywPcGDpxvXvVd%2F8do%2FVsNE%2BjXJ7DuHjtWhaCgvP%2Bj1Z4%2FE%3D",
            "thw": "cn",
            "_tb_token_": "5857611eee15b",
            "xlly_s": "1",
            "mt": "ci=0_0",
            "tracknick": "",
            "cna": "w0JNHE32zB4CAd9CdLbHm106",
            "alitrackid": "re.taobao.com",
            "lastalitrackid": "re.taobao.com",
            "_m_h5_tk": "293849dd057e54c9e04403aac2e00c7d_1675322164551",
            "_m_h5_tk_enc": "82b341e6be56d4f4467576323a266331",
            "v": "0",
            "JSESSIONID": "879DF57846A463FC55B12B2596F3277B",
            "isg": "BN7eZBx5MdIDzmVYjKMVnwdsL3Qgn6IZ_9Yk74hnySE4q36F8ClBKQRKp7enqJox",
            "l": "fBa9efB7TGH7hOpxBO5IPurza779mIRb4lVzaNbMiIEGa1ohOUgECNCeIwBv5dtjgTCfPetPzjfSVdLHR3AJwxDDB3h2q_lS3xv9QaVb5",
            "tfstk": "cjpRBefE3q0uNJuh3Th0TTX-6wgGZX0dlu_3pdRfYx1_spedicpMB7SnNM_NymC.."
        }
        self.client = AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['TaoBao']['info']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        async with ClientSession(headers=self.headers, cookies=self.cookies) as session:
            tasks = []
            for i in range(self.page):
                # 翻页参数从0开始，每页+44
                res = self.parse_data(session, self.url.format(i*44))
                tasks.append(asyncio.create_task(res))
            await asyncio.wait(tasks)

    async def parse_data(self, session: ClientSession, url: str) -> None:
        """
            解析数据

        :param session: aiohttp.ClientSession 对象
        :param url: 当前页地址
        :return: None
        """
        response = await session.get(url)
        resp = await response.text()
        try:
            # 提取页面里的列表数据
            res = re.findall('"auctions":(.*?),"recommendAuctions"', resp)[0]
        except IndexError:
            print('被反爬，请稍后重试..')
            exit()
        res_json = json.loads(res)
        # 遍历列表，获取数据
        for item in res_json:
            info_json = {
                '标题': item['raw_title'],
                '价格': item['view_price'],
                '购买人数': item['view_sales'],
                '地点': item['item_loc'],
                '网址': 'https:{}'.format(item['comment_url']) if item['comment_url'].startswith('//') else item['comment_url'],
                '图片地址': 'https:{}'.format(item['pic_url']) if item['pic_url'].startswith('//') else item['pic_url'],
                '评论数': item['comment_count'],
                '店铺': item['shopName'],
                '店铺地址': 'https:{}'.format(item['shopLink']) if item['shopLink'].startswith('//') else item['shopLink']
            }
            await self.save_data(info_json)

    async def save_data(self, info_json: dict) -> None:
        """
            保存数据到MongoDB数据库
        :param info_json: 每一个商品的数据存在这一个字典里
        :return: None
        """
        await self.collection.insert_one(info_json)
        self.num += 1
        print('保存第 {} 个商品信息成功...'.format(self.num))


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    # 设置获取页数
    page = 20
    tb = TaoBao(page)
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(tb.main())
    print('用时：{} 秒'.format(time.time() - t1))
