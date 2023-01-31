# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  09-多任务爬虫.py
# @Author  ：  jflmao
# @Time    ：  2023-01-23 14:11
# @Software：  PyCharm
# ==============================
"""
    网址：https://so.tv.sohu.com/list_p1101_p2_p3_p4-1_p5_p6_p77_p80_p92_p104_p11_p12_p13_p14.html

    需求：通过多线程队列的方式，获取30页数据信息存储在mongo

    需要的字段：标题，主演，周播放量，集数
"""

import time
from queue import Queue
from threading import Thread

import requests
from lxml import etree
from pymongo import MongoClient


class Sohu(object):
    def __init__(self):
        """
            初始化
        """
        # 连接本地数据库
        self.client = MongoClient('127.0.0.1', 27017)
        # 指定数据库和集合
        self.collection = self.client['SoHu']['sohutv']
        self.url = 'https://so.tv.sohu.com/list_p1101_p2_p3_p4-1_p5_p6_p77_p80_p92_p10{}_p11_p12_p13_p14.html'
        self.headers = {
            'referer': 'https://tv.sohu.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        # 设置三个队列
        self.url_queue = Queue()
        self.data_queue = Queue()
        self.con_queue = Queue()

    def get_url(self, _page: int):
        """
            获取url地址并传入队列

        :param _page: 需要获取的页数
        :return: None
        """
        for i in range(1, _page + 1):
            # 把地址传入队列
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        """
            获取返回数据并传入队列

        :return: None
        """
        while True:
            # 从队列取出URL地址
            url = self.url_queue.get()
            # 请求服务器获取数据
            response = requests.get(url, headers=self.headers)
            response.encoding = "utf-8"
            # 把获取的数据存入队列
            self.data_queue.put(response.text)
            # 从url队列取出的数据已处理完毕
            self.url_queue.task_done()

    def parse_data(self):
        """
            提取需要的数据并存入队列

        :return: None
        """
        while True:
            # 从队列取出网页数据
            data = self.data_queue.get()
            print(data)
            # 将网页字符串转化为Element对象
            html = etree.HTML(data)
            # 获取电视剧列表
            tv_list_data = html.xpath('//ul[@class="st-list cfix"]/li')
            # 遍历列表，提取需要的数据，组合为字典
            for tv_data in tv_list_data:
                tv_list = {
                    '标题': tv_data.xpath('./strong/a/text()')[0],
                    '主演': ' / '.join(tv_data.xpath('./p[@class="actor"]/a/text()')),
                    '周播放量': tv_data.xpath('./p[@class="num-bf"]/text()')[0].split('：')[1],
                    '集数': tv_data.xpath('./div/span/text()')[0]
                }
                # 把字典数据存入队列
                self.con_queue.put(tv_list)
            # 取出的队列数据已处理完毕
            self.data_queue.task_done()

    def save_data(self):
        """
            保存数据到MongoDB数据库

        :return: None
        """
        while True:
            # 从队列取出字典数据
            tv_json = self.con_queue.get()
            # 往数据库存入一行数据
            self.collection.insert_one(tv_json)
            # 取出的队列数据已处理完毕
            self.con_queue.task_done()

    def main(self):
        """
            主方法

        :return: None
        """
        # 指定获取的页数
        page = 30
        # 定义一个线程列表
        thread_list = []
        # 创建一个线程，用于生成URL列表
        t_get_url = Thread(target=self.get_url, args=(page,))
        # 存入线程列表
        thread_list.append(t_get_url)

        # 创建5个线程，用于获取网页数据
        for i in range(10):
            t_get_data = Thread(target=self.get_data)
            thread_list.append(t_get_data)

        # 创建一个线程，用于提取数据
        for i in range(10):
            t_parse_data = Thread(target=self.parse_data)
            thread_list.append(t_parse_data)

        # 创建一个线程，用去保存数据到数据库
        for i in range(10):
            t_save_data = Thread(target=self.save_data)
            thread_list.append(t_save_data)

        # 遍历线程列表，并启动所有线程
        for t in thread_list:
            # 设置子线程守护主线程，主线程结束，子线程也跟着结束
            t.setDaemon(True)
            # 启动线程
            t.start()

        time.sleep(2)
        # 遍历所有队列，如果队列中有数据，则阻塞主线程
        for q in [self.url_queue, self.data_queue, self.con_queue]:
            # 队列阻塞主线程
            q.join()


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    sh = Sohu()
    sh.main()
    print(f'用时：{time.time() - t1}秒')
