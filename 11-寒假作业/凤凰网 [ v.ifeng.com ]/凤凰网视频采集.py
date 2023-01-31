# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  凤凰网视频采集.py
# @Author  ：  jflmao
# @Time    ：  2023-01-28 14:49
# @Software：  PyCharm
# ==============================
"""
    目标：凤凰网视频采集

    网址：https://v.ifeng.com/shanklist/v/27-95283-

    需要：在主页获取到详情页面地址，进入详情页面获取到播放地址，下载视频
"""
import asyncio
import json
import os
import re
import time

from aiofiles import open
from aiohttp import ClientSession, TCPConnector
from motor.motor_asyncio import AsyncIOMotorClient


class IFeng:
    def __init__(self):
        """
            初始化

        """
        # 凤凰网视频地址
        self.url = 'https://v.ifeng.com/shanklist/v/27-95283-'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        # 连接本地MongoDB数据库
        self.client = AsyncIOMotorClient('localhost', 27017)
        # 指定数据库和集合
        self.collection = self.client['ifeng']['video']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        # 忽略SSL证书验证
        conn = TCPConnector(ssl=False)
        async with ClientSession(headers=self.headers, connector=conn) as session:
            # 网络IO，耗时操作，异步挂起
            response = await session.get(self.url)
            # 用正则提取出嵌入网页中 json 内容
            res = re.findall('"videoStream":(.*?),"footer"', await response.text())[0]
            tasks = []
            # 遍历 json 中需要的信息
            for video in json.loads(res):
                video_title = self.replace_special_character(video['title'])
                video_page_url = 'https:{}'.format(video['url'])
                # 获取协程对象并转换成task对象，并提交到事件循环中
                task = asyncio.create_task(self.get_video(session, video_title, video_page_url))
                # 把task对象追加到列表中
                tasks.append(task)
            # 等待所有task对象执行完毕
            await asyncio.wait(tasks)

    async def get_video(self, session: ClientSession, video_title: str, video_page_url: str) -> None:
        """
            获取视频所有信息，并调用保存函数保存

        :param session: aiohttp.ClientSession 对象
        :param video_title: 视频标题
        :param video_page_url: 视频播放页URL地址
        :return: None
        """
        response = await session.get(video_page_url)
        res = re.findall('"https?://ips.ifeng.com/(.*?)"', await response.text())[0]
        video_url = 'https://{}'.format(res)
        response = await session.get(video_url)
        video_data = await response.read()
        await self.save_video(video_data, video_title, video_url)

    async def save_video(self, video_data: bytes, video_title: str, video_url: str) -> None:
        """
            保存视频信息到MongoDB数据库，并把视频下载到本地

        :param video_data: 视频bytes数据
        :param video_title: 视频标题
        :param video_url: 视频URL地址
        :return:
        """
        await self.collection.insert_one({'视频标题': video_title, '视频URL': video_url})
        print('视频信息：{},{} 保存数据库完毕..'.format(video_title,video_url))
        async with open('E:/temp/{}.mp4'.format(video_title), 'wb') as f:
            await f.write(video_data)
            print('视频：{},{} 保存本地完毕..'.format(video_title, video_url))

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
    if not os.path.exists('E:/temp'):
        os.mkdir('E:/temp')
    t1 = time.time()
    ifeng = IFeng()
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(ifeng.main())
    print('用时：{} 秒'.format(time.time() - t1))
