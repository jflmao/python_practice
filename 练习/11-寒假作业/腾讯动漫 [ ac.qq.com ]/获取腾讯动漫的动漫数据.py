# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  获取腾讯动漫的动漫数据.py
# @Author  ：  jflmao
# @Time    ：  2023-02-03 16:47
# @Software：  PyCharm
# ==============================
"""
    网址：https://ac.qq.com/Comic/index/page/
    需求：获取5页数据，获取到漫画的标题、人气、简介、漫画类型
"""
import asyncio
import time

from aiohttp import ClientSession
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


class ACQQ:
    def __init__(self, _page: int):
        """
            初始化

        :param _page: 获取的页数
        """
        self.page = _page
        self.url = 'https://ac.qq.com/Comic/index/page/{}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'
        }
        self.client = AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['ACQQ']['ac']

    async def main(self) -> None:
        """
            主方法
        :return: None
        """
        async with ClientSession(headers=self.headers) as session:
            tasks = []
            for i in range(1, self.page + 1):
                res = self.parse_data(session, self.url.format(i))
                tasks.append(asyncio.create_task(res))
            await asyncio.wait(tasks)

    async def parse_data(self, session: ClientSession, url: str) -> None:
        """
            解析数据

        :param session: aiohttp.ClientSession 对象
        :param url: 动漫列表页URL
        :return: None
        """
        response = await session.get(url)
        html = etree.HTML(await response.text())
        for item in html.xpath('//li[@class="ret-search-item clearfix"]'):
            ac_json = {
                '标题': item.xpath('.//h3[@class="ret-works-title clearfix"]/a/@title')[0],
                '作者': item.xpath('.//p[@class="ret-works-author"]/text()')[0],
                '类型': ' / '.join(item.xpath('.//p[@class="ret-works-tags"]/span[@href]/text()')),
                '人气': '人气：{}'.format(item.xpath('.//p[@class="ret-works-tags"]/span/em/text()')[0]),
                '简介': item.xpath('.//p[@class="ret-works-decs"]/text()')[0],
                '阅读地址': 'https://ac.qq.com{}'.format(item.xpath('.//a[@class="ret-works-view ui-btn-pink"]/@href')[0])
            }
            await self.save_data(ac_json)

    async def save_data(self, ac_json: dict) -> None:
        """
            保存数据到数据库

        :param ac_json: 动漫信息json
        :return: None
        """
        await self.collection.insert_one(ac_json)
        print('保存动漫 《{}》 的信息到MongoDB数据库完成..'.format(ac_json['标题']))


if __name__ == '__main__':
    """
        脚本入口
    """
    # 获取的页数
    page = 5
    t1 = time.time()
    acqq = ACQQ(page)
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(acqq.main())
    print('用时：{} 秒..'.format(time.time() - t1))
