# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  获取到好看视频的视频数据.py
# @Author  ：  jflmao
# @Time    ：  2023-01-30 14:28
# @Software：  PyCharm
# ==============================
"""
    目标：获取到好看视频的视频数据

    网址：https://haokan.baidu.com

    需求：获取到娱乐分类里面的100条视频，下载到本地
"""
import asyncio
import json
import os
import re
import time

from aiofiles import open
from aiohttp import ClientSession, TCPConnector
from motor.motor_asyncio import AsyncIOMotorClient


class HaoKan:
    def __init__(self, _download_path: str):
        """
            初始化

        """
        self.download_path = _download_path
        self.url = 'https://haokan.baidu.com/web/video/feed?tab=yule_new&act=pcFeed&pd=pc&num=20&shuaxin_id={}'.format(int(time.time()) * 10000)
        self.video_page_url = 'https://haokan.baidu.com/v?vid={}&tab=yule_new&sfrom=yule_new '
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Pragma": "no-cache",
            "Referer": "https://haokan.baidu.com/tab/yule_new?sfrom=recommend",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Microsoft Edge\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies = {
            "BAIDUID": "F788A3B9F6477D014A3C8C7724540312:FG=1",
            "BIDUPSID": "F788A3B9F6477D014A3C8C7724540312",
            "PSTM": "1473996812",
            "__yjs_duid": "1_27fe9d7e5c0dac497b9c9fbe1b75edab1624628739864",
            "BDSFRCVID": "G6POJeC62656sO7HRmREuloQ9L5mM4nTH6bHwtHdiGoiijJi8J0WEG0Phf8g0KuMsB3LogKKL2OTHmAF_2uxOjjg8UtVJeC6EG0Ptf8g0f5",
            "H_BDCLCKID_SF": "tbPO_KIatKD3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDk9qfQcy4LdjG5N-xoIKmO7bDQdJ-5SDUDwDRrDeMDB3-Aq5fvy-grQLJTV2f8KMII40bKaQfbQ0-cPqP-jW5Tubhbxbn7JOpvsDxnxy-uFQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ht6IetbKD_D0yJKvKeJbYK4oj5KCyMfca5C6JKCOa3RA8Kb7Vbp0C0MnkbfJBDGDttJJ9J2bNWxoNbRRoVDTsjtcYj-C7yajaBnbJWIn0Kb7V2RckjDn_DhJpQT8rMMDOK5Oibmje5DO1ab3vOp44XpO1hf_zBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDe_K8hJUK",
            "BDSFRCVID_BFESS": "G6POJeC62656sO7HRmREuloQ9L5mM4nTH6bHwtHdiGoiijJi8J0WEG0Phf8g0KuMsB3LogKKL2OTHmAF_2uxOjjg8UtVJeC6EG0Ptf8g0f5",
            "H_BDCLCKID_SF_BFESS": "tbPO_KIatKD3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDk9qfQcy4LdjG5N-xoIKmO7bDQdJ-5SDUDwDRrDeMDB3-Aq5fvy-grQLJTV2f8KMII40bKaQfbQ0-cPqP-jW5Tubhbxbn7JOpvsDxnxy-uFQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ht6IetbKD_D0yJKvKeJbYK4oj5KCyMfca5C6JKCOa3RA8Kb7Vbp0C0MnkbfJBDGDttJJ9J2bNWxoNbRRoVDTsjtcYj-C7yajaBnbJWIn0Kb7V2RckjDn_DhJpQT8rMMDOK5Oibmje5DO1ab3vOp44XpO1hf_zBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDe_K8hJUK",
            "BAIDUID_BFESS": "F788A3B9F6477D014A3C8C7724540312:FG=1",
            "BAIDU_WISE_UID": "wapp_1672822934332_447",
            "ZFY": "ylVpkdkqU:BmDvYJzrvIbqXnyfgWKc4qAIzurj68svj8:C",
            "MCITY": "-316%3A",
            "image_bff_sam": "1",
            "H_PS_PSSID": "36547_37551_37517_38053_36920_37990_37932_38041_26350_37881",
            "delPer": "0",
            "PSINO": "5",
            "BDUSS": "nMxbWl4NW1UbXFDOUFaNjc3dTRmc1JKcTBrNU5rZnNCWlBWNGRTYnJGSXlELTlqSVFBQUFBJCQAAAAAAAAAAAEAAADJLM2dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADKCx2MygsdjZ",
            "BDUSS_BFESS": "nMxbWl4NW1UbXFDOUFaNjc3dTRmc1JKcTBrNU5rZnNCWlBWNGRTYnJGSXlELTlqSVFBQUFBJCQAAAAAAAAAAAEAAADJLM2dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADKCx2MygsdjZ",
            "ZD_ENTRY": "bing",
            "COMMON_LID": "9fcfd9de3eb40fb6364fa9dcbcac5960",
            "Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5": "1674452447",
            "PC_TAB_LOG": "video_details_page",
            "Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5": "1675035348",
            "reptileData": "%7B%22data%22%3A%22b3ce974ee3e02233a206a75614eff55dc8cf7a0ddc15ba180cee2716d7339bc2ea1b3d4f346a0419fc20a30f218b1abcf6c88d70ef5b359bdbb767e2991418e6dc6e73ef071c251097eb2ea6d3f5f91601e8cc9148db3af14e4f916c469bb7cf%22%2C%22key_id%22%3A%2230%22%2C%22sign%22%3A%222d1e35fe%22%7D",
            "ariaDefaultTheme": "undefined",
            "RT": "\"z=1&dm=baidu.com&si=cagaesdy7sb&ss=ldi040jn&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=orxh&ul=cajgf&hd=cajw2\""
        }
        # 连接MongoDB数据库
        self.client = AsyncIOMotorClient('localhost', 27017)
        # 指定数据库和集合
        self.collection = self.client['HaoKanVideo']['video']

    async def main(self) -> None:
        """
            主方法

        :return: None
        """
        # 忽略ssl验证
        conn = TCPConnector(ssl=False)
        # 使用上下文管理器管理实例化的session对象
        async with ClientSession(headers=self.headers, connector=conn, cookies=self.cookies) as session:
            for i in range(5):
                # 获取视频列表
                response = await session.get(self.url)
                res = await response.json(content_type='application/json')
                # 创建task列表
                tasks = []
                try:
                    # 遍历视频列表，获取需要的信息
                    for item in res['data']['response']['videos']:
                        video_id = item['id']
                        video_title = self.replace_special_character(item['title'])
                        # 获取协程对象
                        res = self.get_video(session, self.video_page_url.format(video_id), video_title)
                        # 把协程对象转换成task对象并追加到tasks列表中
                        tasks.append(asyncio.create_task(res))
                except KeyError as e:
                    print('类型错误：{}，内容：{}'.format(e, res))
                # 等待所以task完成
                await asyncio.wait(tasks)

    async def get_video(self, session: ClientSession, video_page_url: str, video_title: str) -> None:
        """
            根据视频地址获取视频

        :param session: aiohttp.ClientSession 对象
        :param video_page_url: 视频播放页地址
        :param video_title: 视频标题
        :return: None
        """
        response = await session.get(video_page_url)
        # 根据视频播放页获取各个清晰度的视频
        res = re.findall('"clarityUrl":(.*?),"video_status"', await response.text())[0]
        video_json = json.loads(res)
        video_list = []
        for video_info in video_json:
            video_list.append({
                '清晰度': video_info['key'],
                "地址": video_info['url']
            })
        await self.save_mongodb(video_title, video_list)
        # 获取最高画质的视频并下载到本地
        response = await session.get(video_json[-1]['url'])
        video_date = await response.read()
        await self.save_video(video_title, video_date)

    async def save_mongodb(self, video_title: str, video_list: list) -> None:
        """
            保存各种清晰度的视频地址，保存到MongoDB数据库

        :param video_title: 视频标题
        :param video_list: 视频列表
        :return: None
        """
        await self.collection.insert_one({
            '视频标题': video_title,
            '视频列表': video_list
        })
        print('保存 {}.mp4 的信息到 MongoDB 数据库成功..'.format(video_title))

    async def save_video(self, video_title: str, video_date: bytes) -> None:
        """
            保存视频到本地

        :param video_title: 视频标题
        :param video_date: 视频字节文件
        :return: None
        """
        async with open('{}/{}.mp4'.format(self.download_path, video_title), 'wb') as f:
            await f.write(video_date)
            print('保存 {}.mp4 最高画质到本地成功...'.format(video_title))

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
    download_path = 'E:/HaoKanVideo'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    t1 = time.time()
    hk = HaoKan(download_path)
    # 获取事件循环并执行
    asyncio.get_event_loop().run_until_complete(hk.main())
    print('用时：{} 秒'.format(time.time() - t1))
