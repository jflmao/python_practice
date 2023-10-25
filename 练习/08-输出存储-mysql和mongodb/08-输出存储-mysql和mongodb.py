# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  08-输出存储-mysql和mongodb.py
# @Author  ：  jflmao
# @Time    ：  2023-01-20 15:02
# @Software：  PyCharm
# ==============================
"""
    目标：
    	获取芒果tv视频电视剧一栏里的电视剧信息，提取名称、集数、描述，获取10个页面，将数据分别存储在mysql和MongoDB数据库

    目标网址：
    	https://www.mgtv.com/lib/2?lastp=list_index&lastp=ch_tv&kind=19&area=10&year=all&sort=c2&chargeInfo=a1&fpa=2912&fpos=
"""

import time

import pymongo
import pymysql
import requests


class Mgtv:
    def __init__(self, _sql='mysql'):
        """
            初始化

        :param _sql: 数据库存储方式
        """
        self.sql = _sql

        # 存储到 mysql
        if self.sql == 'mysql':
            # 连接数据库
            self.db = pymysql.connect(
                host='localhost',
                user='root',
                password=''
            )
            # 创建游标
            self.cursor = self.db.cursor()
            # 如果 mgtv 数据库不存在则创建
            self.cursor.execute('CREATE DATABASE IF NOT EXISTS mgtv')
            # 选择数据库 mgtv
            self.db.select_db('mgtv')
        # 存储到 mongodb
        elif _sql == 'mongodb':
            # 连接数据库
            self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
            # 指定集合
            self.collection = self.client['mgtv']['mgtv']
        else:
            print('存储方式选择错误，请重新输入！')
            return
        self.url = 'https://pianku.api.mgtv.com/rider/list/pcweb/v3'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
        }

    def get_data(self, params):
        """
            获取数据

        :param params: 查询参数
        :return: 返回 json 数据
        """
        # 访问网页
        response = requests.get(self.url, headers=self.headers, params=params)
        # 返回 json
        return response.json()

    def parse_data(self, response):
        """
            提取需要的数据

        :param response: 网页返回的 json 数据
        :return: None
        """
        # 提取列表
        tv_list = response['data']['hitDocs']
        # 遍历需要的内容
        for tv in tv_list:
            item = {
                '名称': tv['title'],
                '集数': tv['updateInfo'],
                '描述': tv['story']
            }
            self.save_data(item)

    def save_data(self, item):
        """
            保存数据

        :param item: 字典数据
        :return: None
        """
        if self.sql == 'mysql':
            # MySQL
            # 插入数据库语句
            sql = 'INSERT INTO mgtv(id, 名称, 集数, 描述) values(%s, %s, %s, %s)'
            try:
                # 执行数据库语句
                self.cursor.execute(sql, (0, item['名称'], item['集数'], item['描述']))
                # 提交
                self.db.commit()
            except Exception as e:
                print(f'数据插入失败: {e}')
                # 回滚
                self.db.rollback()
        else:
            # MongoDB
            # 插入一行数据
            self.collection.insert_one(item)

    def create_table(self):
        """
            创建数据表

        :return: None
        """
        sql = '''
            CREATE TABLE IF NOT EXISTS mgtv(
                id int primary key auto_increment not null,
                名称 VARCHAR(255) NOT NULL, 
                集数 VARCHAR(255) NOT NULL, 
                描述 TEXT)
            '''
        try:
            self.cursor.execute(sql)
            print("创建数据表成功。")
        except Exception as e:
            print(f"创建数据表失败：{e}")

    def main(self):
        """
            主函数

        :return: None
        """
        if self.sql == 'mysql':
            # MySQL
            # 创建数据表
            self.create_table()

        # 指定获取的页数
        page = 10
        for i in range(1, page + 1):
            params = {
                'allowedRC': '1',
                'platform': 'pcweb',
                'channelId': '2',
                'pn': str(i),
                'pc': '80',
                'hudong': '1',
                '_support': '10000000',
                'kind': '19',
                'area': '10',
                'year': 'all',
                'chargeInfo': 'a1',
                'sort': 'c2'
            }
            response = self.get_data(params)
            self.parse_data(response)

        if self.sql == 'mysql':
            # 关闭数据库连接
            self.db.close()


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    # mgtv = Mgtv('mysql')
    mgtv = Mgtv('mongodb')
    mgtv.main()
    print(f'耗时：{time.time() - t1} 秒')
