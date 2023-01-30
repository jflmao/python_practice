# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  B站评论采集.py
# @Author  ：  jflmao
# @Time    ：  2023-01-26 11:44
# @Software：  PyCharm
# ==============================
"""
    目标：B站评论采集

    网址：https://www.bilibili.com/video/BV1FM411F7rH/?spm_id_from=333.337.search-card.all.click&vd_source=2e399ef6e2389d3f4bfdddc5315d33da

    需求：获取到当前地址的评论数据
"""
import asyncio
import re
import time

from aiohttp import ClientSession
from motor import motor_asyncio


class BiLiBiLi:
    def __init__(self):
        """
            初始化
        """
        self.video_url = 'https://www.bilibili.com/video/BV1FM411F7rH/?spm_id_from=333.337.search-card.all.click&vd_source=2e399ef6e2389d3f4bfdddc5315d33da'
        self.replies_list_url = 'https://api.bilibili.com/x/v2/reply/main?mode=3&next={}&oid={}&plat=1&type=1'
        self.floor_replies_list_url = 'https://api.bilibili.com/x/v2/reply/reply?oid={}&pn={}&ps=10&root={}&type=1'
        self.headers = {
            'referer': 'https://www.bilibili.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        self.client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.collection = self.client['bilibili']['replies']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        # 使用上下文管理器实例化 ClientSession 类
        async with ClientSession(headers=self.headers) as session:
            # 请求视频地址，获取下一步需要的关键参数
            response = await session.get(self.video_url)
            res = await response.text()
            # 获取关键参数 oid
            oid_para = re.findall('"stat":{"aid":(.*?),', res)[0]
            # 获取全部评论数
            all_reply = int(re.findall('"reply":(.*?),', res)[0])
            tasks = []
            # all_reply是总评论数，每页20条，就对20取余，如果有余数就+1，而range是包前不包后，所以需要再+1
            all_reply = all_reply // 20 + 2 if all_reply % 20 else all_reply // 20 + 1
            for page in range(1, all_reply):
                # 获取协程对象
                res = self.get_replies(session, page, oid_para)
                # 把协程对象转换成task对象
                task = asyncio.create_task(res)
                tasks.append(task)
            await asyncio.wait(tasks)

    async def get_replies(self, session: ClientSession, next_para: int, oid_para: str) -> None:
        """
            获取视频下的评论

        :param session: aiohttp.ClientSession 对象
        :param next_para: 页数
        :param oid_para: URL中的 oid 参数
        :return: None
        """
        # 延迟1秒
        await asyncio.sleep(2)
        url = self.replies_list_url.format(next_para, oid_para)
        response = await session.get(url)
        res = await response.json(content_type='application/json')
        if res['code'] == -412:
            print('已被反爬程序发现，{}..'.format(res['message']))
            return
        # 如果获取到的评论列表数为0，则直接返回
        if len(res['data']['replies']) == 0:
            return
        try:
            for reply in res['data']['replies']:
                reply_dict = {
                    '用户名': reply['member']['uname'],
                    '时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(reply['ctime'])),
                    '点赞数': reply['like'],
                    '评论内容': reply['content']['message'],
                    '被评论数': reply['rcount'],
                    '被评论内容': []
                }
                await self.get_child_replies(session, reply['rcount'], oid_para, reply['rpid'], reply_dict)
        except TypeError as e:
            print('类型错误：{}，地址：{}'.format(e, url))

    async def get_child_replies(self, session: ClientSession, rcount: int, oid_para: str, root_para: int, reply_dict: dict) -> None:
        """
            获取所有子评论

        :param session: aiohttp.ClientSession 对象
        :param rcount: 楼中楼评论总数
        :param oid_para: URL中的 oid 参数
        :param root_para: 父评论的pid
        :param reply_dict: 字典类型的评论信息
        :return: None
        """
        if rcount > 0:
            # rcount是总评论数，每页10条，就对10取余，如果有余数就+1，而range是包前不包后，所以需要再+1
            rcount = rcount // 10 + 2 if rcount % 10 else rcount // 10 + 1
            for page in range(1, rcount):
                await asyncio.sleep(2)
                url = self.floor_replies_list_url.format(oid_para, page, root_para)
                response = await session.get(url)
                res = await response.json(content_type='application/json')
                if res['code'] == -412:
                    print('已被反爬程序发现，{}...'.format(res['message']))
                    return
                try:
                    for reply in res['data']['replies']:
                        reply_dict['被评论内容'].append({
                            '用户名': reply['member']['uname'],
                            '时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(reply['ctime'])),
                            '点赞数': str(reply['like']),
                            '评论内容': reply['content']['message']
                        })
                except TypeError as e:
                    print('类型错误：{}，地址：{}'.format(e, url))
        await self.save_replies(reply_dict)

    async def save_replies(self, reply_dict: dict) -> None:
        """
            保存字典类型的评论信息到 MongoDB 数据库

        :param reply_dict: 字典类型的评论信息
        :return: None
        """
        await self.collection.insert_one(reply_dict)


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    # 实例化
    bilibili = BiLiBiLi()
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(bilibili.main())
    print('用时：{} 秒'.format(time.time() - t1))
