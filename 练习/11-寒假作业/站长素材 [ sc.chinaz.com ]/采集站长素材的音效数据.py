# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  采集站长素材的音效数据.py
# @Author  ：  jflmao
# @Time    ：  2023-02-03 7:23
# @Software：  PyCharm
# ==============================
"""
    网址：https://sc.chinaz.com/yinxiao/index_1.html
    需求：获取5页的音频数据
"""
import asyncio
import os
import time

from aiofiles import open
from aiohttp import ClientSession
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


class ChinaZ:
    def __init__(self, _page: int, _download_path: str):
        """
            初始化

        :param _page: 需要获取的页数
        :param _download_path: 下载保存路径
        """
        self.page = _page
        self.download_path = _download_path
        self.url = 'https://sc.chinaz.com/yinxiao/index_{}.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'
        }
        self.client = AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['ChinaZ']['yinxiao']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        async with ClientSession(headers=self.headers) as session:
            tasks = []
            for p in range(1, self.page + 1):
                coro_obj = self.parse_data(session, self.url.format(p))
                tasks.append(asyncio.create_task(coro_obj))
            await asyncio.wait(tasks)

    async def parse_data(self, session: ClientSession, url: str) -> None:
        """
            解析数据

        :param session: aiohttp.ClientSession 对象
        :param url: 音效列表页地址
        :return: None
        """
        response = await session.get(url)
        html = etree.HTML(await response.text())
        for item in html.xpath('//div[@class="audio-item"]'):
            yx_json = {
                '名字': item.xpath('.//p[@class="name"]/text()')[0].strip(),
                '分类': ' / '.join([x.strip() for x in item.xpath('.//div[@class="audio-class"]/a/text()')]),
                '时长': item.xpath('.//div[@class="audio-time"]/p/text()')[0],
                '下载地址': 'https:{}'.format(item.xpath('.//audio/@src')[0])}
            await self.save_data(session, yx_json)

    async def save_data(self, session: ClientSession, yx_json: dict) -> None:
        """
            保存音效数据

        :param session: aiohttp.ClientSession 对象
        :param yx_json: 音效信息JSON
        :return: None
        """
        try:
            await self.collection.insert_one(yx_json)
            print('保存 “{}” 音效数据到MongoDB数据库成功..'.format(yx_json['名字']))
        except Exception as e:
            print('保存 “{}” 音效数据到MongoDB数据库失败：{}:{}..'.format(yx_json['名字'], e.__class__.__name__, e))
            return
        res = await session.get(yx_json['下载地址'])
        yx_data = await res.read()
        async with open('{}/{}.mp3'.format(self.download_path, yx_json['名字']), 'wb') as f:
            try:
                await f.write(yx_data)
                print('保存 “{}” 音效数据到本地成功..'.format(yx_json['名字']))
            except Exception as e:
                print('保存 “{}” 音效数据到本地失败：{}:{}..'.format(yx_json['名字'], e.__class__.__name__, e))
                return


if __name__ == '__main__':
    """
        脚本入口
    """
    # 需要获取的页数
    page = 5
    # 下载地址
    download_path = 'E:/音效'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    t1 = time.time()
    cz = ChinaZ(page, download_path)
    asyncio.get_event_loop().run_until_complete(cz.main())
    print('用时：{} 秒..'.format(time.time() - t1))
