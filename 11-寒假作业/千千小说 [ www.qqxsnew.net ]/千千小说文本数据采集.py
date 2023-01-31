# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  千千小说文本数据采集.py
# @Author  ：  jflmao
# @Time    ：  2023-01-28 20:21
# @Software：  PyCharm
# ==============================
"""
    目标：千千小说文本数据采集

    网址：https://www.qqxsnew.net/12/12776/

    需求：获取到当前小说的所有章节保存在本地文件
"""
import asyncio
import os
import time

from aiofiles import open
from aiohttp import ClientSession, TCPConnector
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


class QQxs:
    def __init__(self):
        self.url = 'https://www.qqxsnew.net/12/12776/'
        self.chapter_url = 'https://www.qqxsnew.net{}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        self.client = AsyncIOMotorClient('localhost', 27017)
        self.collection = None

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        # 忽略SSL证书验证
        conn = TCPConnector(ssl=False)
        async with ClientSession(headers=self.headers, connector=conn) as session:
            response = await session.get(self.url)
            html = etree.HTML(await response.text())
            # 获取小说名字
            fiction_name = html.xpath('//h1/text()')[0]
            # 指定以小说名字命名的集合
            self.collection = self.client['QQXS'][fiction_name]
            tasks = []
            for chapter in html.xpath('//dt[2]//following-sibling::dd'):
                chapter_name = chapter.xpath('./a/text()')[0]
                chapter_url = self.chapter_url.format(chapter.xpath('./a/@href')[0])
                res = self.get_chapter(session, chapter_url, chapter_name, fiction_name)
                tasks.append(asyncio.create_task(res))
            await asyncio.wait(tasks)

    async def get_chapter(self, session: ClientSession, chapter_url: str, chapter_name: str, fiction_name: str) -> None:
        """
            获取章节信息

        :param session: aiohttp.ClientSession 对象
        :param chapter_url: 章节URL地址
        :param chapter_name: 章节名字
        :param fiction_name: 小说名字
        :return: None
        """
        response = await session.get(chapter_url)
        html = etree.HTML(await response.text(encoding='utf-8'))
        # 处理小说内容，去掉尾部广告
        chapter_txt = '\r\n'.join(html.xpath('//div[@id="content"]/text()')).split('无尽的昏迷过后')[0]
        await self.save_chapter(chapter_name, chapter_url, chapter_txt, fiction_name)

    async def save_chapter(self, chapter_name: str, chapter_url: str, chapter_txt: str, fiction_name: str) -> None:
        """
            保存章节

        :param chapter_name: 章节名字
        :param chapter_url: 章节URL地址
        :param chapter_txt: 章节内容
        :param fiction_name: 小说名字
        :return: None
        """
        await self.collection.insert_one({'章节': chapter_name, '章节URL': chapter_url})
        print('保存小说《{}》{} 的URL地址到MongoDB数据库成功..'.format(fiction_name, chapter_name))
        fiction_path = '{}/{}'.format(download_path, fiction_name)
        chapter_path = '{}/{}.txt'.format(fiction_path, self.replace_special_character(chapter_name))
        if not os.path.exists(fiction_path):
            os.mkdir(fiction_path)
        # 需要指定编码格式，不然有些章节会写入报错
        async with open(chapter_path, 'w', encoding='utf-8') as f:
            await f.write(chapter_txt)
            # print('保存小说《{}》{} 成功...'.format(fiction_name, chapter_name))

    @staticmethod
    def replace_special_character(text: str) -> str:
        """
            替换一些文件路径中的非法字符

        :param text: 需要替换的字符串
        :return: 替换好的字符串
        """
        text = text.replace('\\', '-')
        text = text.replace('/', '-')
        text = text.replace(':', '：')
        text = text.replace('*', '#')
        text = text.replace('?', '？')
        text = text.replace('<', '《')
        text = text.replace('>', '》')
        text = text.replace('|', '-')
        text = text.replace('"', '“')
        return text


if __name__ == '__main__':
    """
        脚本入口
    """
    download_path = 'E:/小说'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    t1 = time.time()
    qqxs = QQxs()
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(qqxs.main())
    print('用时：{} 秒'.format(time.time() - t1))
