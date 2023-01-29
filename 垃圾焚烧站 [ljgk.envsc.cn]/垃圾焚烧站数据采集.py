# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  垃圾焚烧站数据采集.py
# @Author  ：  jflmao
# @Time    ：  2023-01-29 12:49
# @Software：  PyCharm
# ==============================
"""
    目标：垃圾焚烧站数据采集

    网址：https://ljgk.envsc.cn/

    需求：获取到焚烧站的地址、公司名称
"""
import time

import pymongo
import requests


class LJFSZ:
    def __init__(self):
        self.url = 'https://ljgk.envsc.cn/OutInterface/GetPSList.ashx?regionCode=0&psname=&SystemType=C16A882D480E678F&sgn=f4b20434f3dca4d918d2e993c751b525c2a8fe49&ts=1674968794853&tc=67973770'
        self.headers = {
            'Referer': 'https://ljgk.envsc.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }
        self.client = pymongo.MongoClient('localhost', 27017)
        self.collection = self.client['LJFSZ']['info']

    def main(self):
        """
            主方法

        :return: None
        """
        with requests.Session() as session:
            response = session.get(self.url, headers=self.headers)
            for item in response.json():
                name = item['ps_name']
                address = '{}，{}'.format(item['fullregion_name'], item['address'])
                self.collection.insert_one({
                    '公司': name,
                    '地址': address
                })


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    ljfsz = LJFSZ()
    ljfsz.main()
    print('用时：{} 秒'.format(time.time() - t1))
