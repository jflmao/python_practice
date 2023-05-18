# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  采集网易新闻数据.py
# @Author  ：  jflmao
# @Time    ：  2023-02-03 13:39
# @Software：  PyCharm
# ==============================
"""
    网址：https://c.m.163.com/news/hot/newsList
    需求：获取到当前进入详情页面的a标签，提取详情页面的文本数据
"""
import asyncio
import re
import time

from aiohttp import ClientSession
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


class M163:
    def __init__(self):
        """
            初始化
        """
        self.url = 'https://c.m.163.com/news/hot/newsList'
        # 由于网址是手机端的，所以请求头的UA用手机版的
        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/109.0.0.0'
        }
        self.client = AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['M163']['news']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        async with ClientSession(headers=self.headers) as session:
            response = await session.get(self.url)
            htm = await response.text()
            html = etree.HTML(htm)
            tasks = []
            # 用 xpath 获取新闻列表，并遍历获取需要的信息
            for item in html.xpath('//div[@class="title"]'):
                url = item.xpath('./a/@href')[0]
                # 剔除掉URL中含有'/v/'的只有视频没有文章内容的新闻
                if '/v/' in url:
                    continue
                title = item.xpath('./a/text()')[0]
                coro_obj = self.parse_data(session, title, url)
                tasks.append(asyncio.create_task(coro_obj))
            await asyncio.wait(tasks)

    async def parse_data(self, session: ClientSession, title: str, url: str) -> None:
        """
            解析数据，获取新闻内容

        :param session: aiohttp.ClientSession 对象
        :param title: 新闻标题
        :param url: 新闻URL
        :return: None
        """
        response = await session.get(url)
        res = re.findall('},"body":"(.*?)","originalTitle"', await response.text())[0]
        # 中文字符串中夹杂 unicode 形式字符串如 '\u5403\u9e21战场'，可用如下方式转码
        res = res.encode('raw_unicode_escape').decode('unicode_escape')
        text = '\r\n'.join(etree.HTML(res).xpath('//p/text()'))
        await self.save_bata(title, text)

    async def save_bata(self, title: str, text: str) -> None:
        """
            保存数据到MongoDB数据库

        :param title: 新闻标题
        :param text: 新闻内容
        :return: None
        """
        await self.collection.insert_one({
            '标题': title,
            '内容': text
        })
        print('新闻 {} 保存数据库完毕..'.format(title))


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    m163 = M163()
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(m163.main())
    print('用时：{} 秒..'.format(time.time() - t1))
