# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  360图片采集.py
# @Author  ：  jflmao
# @Time    ：  2023-01-25 21:24
# @Software：  PyCharm
# ==============================
"""
    目标：360图片数据

    网址：https://image.so.com/i?q=python&src=&inact=0

    需求：根据给定的关键字获取图片，获取3页数据
"""
import asyncio
import os
import time

from aiohttp import ClientSession
from motor import motor_asyncio


class San60_Image:
    def __init__(self, _page):
        """
            初始化

        :param _page: 需要获取的页数
        """
        self.page = _page
        self.url = 'https://image.so.com/j?q=python&pn=60&sn={}&ps={}&pc={}&_=' + str(int(time.time() * 1000))
        self.headers = {
            'referer': 'https://image.so.com/i?q=python&src=&inact=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        # 连接数据库
        self.client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        # 指定数据库和集合
        self.collection = self.client['SAN60']['image']

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

    async def save_image_info(self, image_title: str, image_url: str) -> None:
        """
            保存图片信息到本地 MongoDB 数据库

        :param image_title: 图片 name
        :param image_url: 图片 url
        :return: None
        """
        # 使用第三方异步 MongoDB 操作模块进行保存
        await self.collection.insert_one({
            '标题': image_title,
            'URL': image_url
        })
        print('保存 {}：{} 完成...'.format(image_title, image_url))

    async def parse_image_info(self, image_info_list: list) -> None:
        """
            处理图片信息，获取需要的信息

        :param image_info_list: 图片信息列表
        :return: None
        """
        # 遍历图片列表，获取需要的信息
        for image_info in image_info_list:
            # 获取图片标题并替换非法字符
            image_title = self.replace_special_character(image_info['title'])
            # 获取图片URL地址
            image_url = image_info['img']
            await self.save_image_info(image_title, image_url)

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        # 使用上下文管理器实例化 ClientSession 类
        async with ClientSession(headers=self.headers) as session:
            # 创建一个 Task 对象列表
            tasks = []
            sn = ps = pc = 0
            for i in range(1, self.page + 1):
                # 网页请求获取URL列表，耗时操作，需要异步挂起
                response = await session.get(self.url.format(sn, ps, pc))
                res = await response.json(content_type='application/javascript')
                # 获取翻页参数
                sn = res['lastindex']
                ps = res['ps']
                pc = res['pc']
                # 获取图片列表
                image_info_list = res['list']
                # 获取协程对象
                res = self.parse_image_info(image_info_list)
                # 把协程对象转换成Task对象
                task = asyncio.create_task(res)
                # 把Task对象追加到列表里
                tasks.append(task)
            # 等待所有Task完成
            await asyncio.wait(tasks)


if __name__ == '__main__':
    """
        脚本入口
    """
    # 指定获取的页数
    page = 3
    t1 = time.time()
    # 类的实例化
    s60 = San60_Image(page)
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(s60.main())
    print('用时：{} 秒'.format(time.time() - t1))
