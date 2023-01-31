# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  10-异步请求作业.py
# @Author  ：  jflmao
# @Time    ：  2023-01-24 14:48
# @Software：  PyCharm
# ==============================
"""
    要求：通过异步的方式获取到英雄联盟官网的英雄皮肤图片

    网址：https://101.qq.com/#/hero
"""

import asyncio
import os
import time

import aiohttp
from aiofiles import open
from motor import motor_asyncio


class YXLM:
    def __init__(self):
        """
            初始化
        """
        # 获取英雄列表的
        self.hero_list_url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts={}'
        # 获取皮肤列表
        self.hero_skins_list_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js?ts={}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        # 连接本地数据库，使用第三方 MongoDB 异步模块 motor
        self.client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        # 指定数据库和集合
        self.collection = self.client['YXLM']['hero_skins']

    async def download_image(self, session: aiohttp.ClientSession, hero_name: str, skin_name: str, skin_url: str) -> None:
        """
            下载图片保存到本地，并把皮肤信息保存到 MongoDB 数据库

        :param session: aiohttp.ClientSession 对象
        :param hero_name: 英雄的名字
        :param skin_name: 皮肤的名字
        :param skin_url: 皮肤图片的地址
        :return: None
        """
        skin_info = {
            '英雄': hero_name,
            '皮肤名': skin_name,
            '皮肤url': skin_url
        }
        # 异步存储到 MongoDB 数据库
        await self.collection.insert_one(skin_info)
        # 如果 image 目录下没有以英雄名命名的文件夹则创建
        if not os.path.exists(f'image/{hero_name}'):
            os.mkdir(f'image/{hero_name}')
        # 如果以英雄名命名的文件夹下没有指定的皮肤图片则下载保存
        if not os.path.exists(f'image/{hero_name}/{skin_name}.jpg'):
            # 获取指定的皮肤图片，耗时操作，需要异步挂起
            response = await session.get(skin_url)
            hero_image = await response.read()
            # 使用 aiofiles 异步操作文件模块进行保存
            async with open(f'image/{hero_name}/{skin_name}.jpg', 'wb') as f:
                await f.write(hero_image)
                global num
                num += 1
                print('下载 “{}” 的 “{}” 皮肤完成。'.format(hero_name, skin_name))

    async def get_big_image(self, session: aiohttp.ClientSession, hero_id: str) -> None:
        """
            获取皮肤原始图片地址

        :param session: aiohttp.ClientSession 对象
        :param hero_id: 英雄ID
        :return: None
        """
        # 获取皮肤列表，耗时操作，需要异步挂起，第二个参数是URL中的 ts 参数，这个是秒级时间戳除以600得到，就是说每10分钟变一次，不过不用这个参数也可以
        response = await session.get(self.hero_skins_list_url.format(hero_id, int(time.time() // 600)))
        # 响应头中 content_type 的值是 'application/x-javascript'，所以这里要指定一下，否则报错，也可以指定为 'None'
        hero_json = await response.json(content_type='application/x-javascript')
        # 遍历皮肤列表，提取需要的信息
        for skin_info in hero_json['skins']:
            if skin_info['mainImg'] != '':
                hero_name = skin_info['heroTitle']
                # 有点皮肤名里包含‘/’，无法创建文件夹，需要替换
                skin_name = skin_info['name'].replace('/', '-').replace(':', '：').replace('"', '”')
                skin_url = skin_info['mainImg']
                # 调用下载方法进行下载，耗时操作，需要异步挂起
                await self.download_image(session, hero_name, skin_name, skin_url)

    async def main(self):
        """
            主方法
        :return: None
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            # 网页请求为耗时操作，用 await 异步挂起，第二个参数是URL中的 ts 参数，这个是秒级时间戳除以600得到，就是说每10分钟变一次，不过不用这个参数也可以
            response = await session.get(self.hero_list_url.format(int(time.time() // 600)))
            # 响应头中 content_type 的值是 'application/x-javascript'，所以这里要指定一下，否则报错，也可以指定为 'None'
            yxlm_json = await response.json(content_type='application/x-javascript')
            # 创建一个 Task 对象列表
            task_list = []
            for hero in yxlm_json['hero']:
                # 遍历出 英雄ID
                hero_id = hero['heroId']
                # 获取协程对象
                res = self.get_big_image(session, hero_id)
                # 把协程对象转换成 Task 对象
                task = asyncio.create_task(res)
                task_list.append(task)
            # 等待所有 Task 完成
            await asyncio.wait(task_list)


if __name__ == '__main__':
    """
        脚本入口
    """
    num = 0
    # 如果脚本目录下没有 image 文件夹则创建
    if not os.path.exists('image'):
        os.mkdir('image')
    t1 = time.time()
    # 实例化
    yxlm = YXLM()
    # 获取事件循环 loop
    loop = asyncio.get_event_loop()
    # 使用事件循环执行协程
    loop.run_until_complete(yxlm.main())
    print('共下载：{} 个皮肤图片'.format(num))
    print('用时：{} 秒'.format(time.time() - t1))
