# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  3G壁纸采集.py
# @Author  ：  jflmao
# @Time    ：  2023-01-24 22:15
# @Software：  PyCharm
# ==============================
"""
    目标：3G壁纸

    网址：https://www.3gbizhi.com/wallDM/index_2.html

    需求：获取当前网址上3页壁纸数据
"""
import asyncio
import time

from aiohttp import ClientSession
from fake_useragent import UserAgent
from lxml import etree
from motor import motor_asyncio


class SanGbizhi:
    def __init__(self, _page: int) -> None:
        """
            初始化

        :param _page: 指定需要下载的页数
        """
        self.page = _page
        # 实例化随机UA类，指定生成 chrome 内核的 UA
        self.ua = UserAgent(browsers=['chrome'])
        self.url = 'https://www.3gbizhi.com/wallDM/index{}.html'
        self.headers = {
            'Referer': 'https://www.3gbizhi.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        self.client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['SanGBiZhi']['image']

    async def save_image_info(self, image_name: str, image_url: str) -> None:
        """
            保存图片信息到本地 MongoDB 数据库

        :param image_name: 图片 name
        :param image_url: 图片 url
        :return: None
        """
        # 使用第三方异步 MongoDB 操作模块进行保存
        await self.collection.insert_one({
            '标题': image_name,
            'URL': image_url
        })
        print('保存 {}：{} 完成...'.format(image_name, image_url))

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        # 使用上下文管理器实例化 Session
        async with ClientSession(headers=self.headers) as session:
            # 更新随机UA
            session.headers.update({'User-Agent': self.ua.random})
            for i in range(1, self.page + 1):
                # 处理URL翻页部分
                if i == 1:
                    i = ''
                else:
                    i = '_{}'.format(i)
                # 网页请求列表数据，耗时操作，需要异步挂起
                response = await session.get(self.url.format(i))
                res = await response.text()
                # 将网页字符串转化为Element对象
                html = etree.HTML(res)
                # 获取图片列表
                image_list_xpath = html.xpath('//div[@class="contlistw mtw"]/ul[@class="cl"]/li')
                # 创建 Task 对象列表
                tasks = []
                # 遍历图片列表，获取每张图片的信息
                for image_info in image_list_xpath:
                    # 获取图片名
                    image_name = image_info.xpath('.//img/@title')[0]
                    # 获取图片url
                    image_url = image_info.xpath('.//img/@lazysrc')[0].split('.jpg')[0] + '.jpg'
                    # 获取协程对象
                    res = self.save_image_info(image_name, image_url)
                    # 把协程对象转换成 Task 对象
                    task = asyncio.create_task(res)
                    # 把 Task 对象追加到列表中
                    tasks.append(task)
                # 等待所有 Task 完成
                await asyncio.wait(tasks)


if __name__ == '__main__':
    """
        脚本入口
    """
    # 指定获取的页数
    page = 3
    # 记录开始时间
    t1 = time.time()
    # 类的实例化
    sg = SanGbizhi(page)
    # 获取事件循环
    loop = asyncio.get_event_loop()
    # 使用事件循环执行协程
    loop.run_until_complete(sg.main())
    print('用时：{}'.format(time.time() - t1))
