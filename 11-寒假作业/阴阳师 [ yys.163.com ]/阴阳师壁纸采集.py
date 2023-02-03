# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  阴阳师壁纸采集.py
# @Author  ：  jflmao
# @Time    ：  2023-02-03 22:37
# @Software：  PyCharm
# ==============================
"""
    网址：https://yys.163.com/media/picture.html
    需求：获取到阴阳师所有的壁纸图片
"""
import asyncio
import os
import time

from aiofiles import open
from aiohttp import ClientSession
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


class YYS:
    def __init__(self, _download_path: str):
        """
            初始化
        :param _download_path: 下载路径
        """
        self.download_path = _download_path
        self.url = 'https://yys.163.com/media/picture.html'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'
        }
        self.client = AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['YYS']['image']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        async with ClientSession(headers=self.headers) as session:
            response = await session.get(self.url)
            html = etree.HTML(await response.text())
            tasks = []
            # 遍历图片列表
            for i, mask in enumerate(html.xpath('//div[@class="mask"]')):
                image_json = {'图片名': 'image{}'.format(i), 'URL': []}
                # 遍历同一张图片的不同分辨率版本
                for image in mask.xpath('./a'):
                    image_json['URL'].append(image.xpath('./@href')[0])
                coro_obj = self.get_image(session, image_json, 'image{}'.format(i))
                tasks.append(asyncio.create_task(coro_obj))
            await asyncio.wait(tasks)

    async def get_image(self, session: ClientSession, image_json: dict, image_name: str) -> None:
        """
            获取图片

        :param session: aiohttp.ClientSession 对象
        :param image_json: 图片信息json
        :param image_name: 图片名字
        :return: None
        """
        await self.save_image_to_mongodb(image_json, image_name)
        for image_url in image_json['URL']:
            response = await session.get(image_url)
            image_bytes = await response.read()
            await self.save_image_to_hdisk(image_bytes, image_name, image_url)

    async def save_image_to_mongodb(self, image_json: dict, image_name: str) -> None:
        """
            保存图片信息到MongoDB数据库

        :param image_json: 图片信息json
        :param image_name: 图片名字
        :return: None
        """
        await self.collection.insert_one(image_json)
        print('保存 {} 到MongoDB数据库完成..({})'.format(image_name, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

    async def save_image_to_hdisk(self, image_bytes: bytes, image_name: str, image_url: str) -> None:
        """
            保存图片到硬盘

        :param image_bytes: 二进制编码格式的图片
        :param image_name: 图片名字
        :param image_url: 图片URL
        :return: None
        """
        save_path = '{}/{}/{}'.format(self.download_path, image_name, image_url.split('/')[-1])
        async with open(save_path, 'wb') as f:
            await f.write(image_bytes)
            print('下载 {}：{} 成功...({})'.format(image_name, image_url, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))


if __name__ == '__main__':
    """
        脚本入口
    """
    download_path = 'E:/阴阳师'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    t1 = time.time()
    yys = YYS(download_path)
    asyncio.get_event_loop().run_until_complete(yys.main())
    print('用时：{} 秒..'.format(time.time() - t1))
