# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  13-免费ip采集测试.py
# @Author  ：  jflmao
# @Time    ：  2023-02-08 19:04
# @Software：  PyCharm
# ==============================
"""
    采集快代理30页ip数据进行测试，获取到有效的ip地址

    网址：https://www.kuaidaili.com/free/
"""
import asyncio
import time

from aiohttp import ClientSession
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


class KuaiDaiLi:
    def __init__(self, _page):
        """
            初始化

        :param _page: 需要获取的页数
        """
        self.page = _page
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.check_url = 'http://httpbin.org/ip'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'
        }
        # 连接本地MongoDB数据库，并指定数据库和集合
        client = AsyncIOMotorClient('localhost', 27017)
        self.collection = client['KuaiDaiLi']['free']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        async with ClientSession(headers=self.headers) as session:
            tasks = []
            for i in range(1, self.page + 1):
                response = await session.get(self.url.format(i))
                html = etree.HTML(await response.text())
                for ip in html.xpath('//tr[td]'):
                    ips = {
                        'IP': ip.xpath('./td[@data-title="IP"]/text()')[0],
                        'PORT': ip.xpath('./td[@data-title="PORT"]/text()')[0],
                        '匿名度': ip.xpath('./td[@data-title="匿名度"]/text()')[0],
                        '类型': ip.xpath('./td[@data-title="类型"]/text()')[0],
                        '位置': ip.xpath('./td[@data-title="位置"]/text()')[0],
                        '响应速度': ip.xpath('./td[@data-title="响应速度"]/text()')[0],
                        '付费方式': ip.xpath('./td[@data-title="付费方式"]/text()')[0]
                    }
                    # 获取协程对象
                    coro_obj = self.check_ip(session, ips)
                    # 把协程对象转换成Task对象，并追加到列表
                    tasks.append(asyncio.create_task(coro_obj))
                # 等待事件循环结束
                await asyncio.wait(tasks)

    async def check_ip(self, session: ClientSession, ips: dict) -> None:
        """
            检查代理IP是否有效

        :param session: aiohttp.ClientSession 对象
        :param ips: 获取的字典类型的ip信息
        :return: None
        """
        # 检查代理IP计数
        global check_ip_num
        check_ip_num += 1
        ip = '{}:{}'.format(ips['IP'], ips['PORT'])
        proxies = 'http://' + ip
        try:
            response = await session.get(self.check_url, proxy=proxies, timeout=3)
            res = await response.text()
            if 'origin' in res:
                print('{} 可用..\r\n'.format(res))
                # 有效代理IP计数
                global ip_num
                ip_num += 1
                await self.save(ips)
        except Exception as e:
            print('验证错误：{}: {}'.format(e.__class__.__name__, e))

    async def save(self, ips) -> None:
        """
            保存有效的代理IP

        :param ips: 有效的IP信息（字典）
        :return: None
        """
        # 如果不存在就保存
        if await self.collection.find_one(ips) is None:
            await self.collection.insert_one(ips)


if __name__ == '__main__':
    """
        脚本入口
    """
    # 检查代理IP计数
    check_ip_num = 0
    # 有效代理IP计数
    ip_num = 0
    # 获取的页数
    page = 30
    t1 = time.time()
    kdl = KuaiDaiLi(page)
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(kdl.main())
    print('用时：{} 秒..'.format(time.time() - t1))
    print('共测试 {} 个IP，{} 个可用..'.format(check_ip_num, ip_num))
