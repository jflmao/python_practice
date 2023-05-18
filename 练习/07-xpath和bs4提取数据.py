# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  07-xpath和bs4提取数据.py
# @Author  ：  jflmao
# @Time    ：  2023-01-19 20:17
# @Software：  PyCharm
# ==============================
import requests

from bs4 import BeautifulSoup
from lxml import etree

"""
    1. 网址：http://ip.yqie.com/ipproxy.htm
    用bs4来做一个简单的爬虫，爬取某个ip网址里的免费ip，获取每个ip的代理IP地址、端口、服务器地址、是否匿名、类型、存活时间
"""


def zuoye1():
    url = 'http://ip.yqie.com/ipproxy.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    ip_infos = soup.select('tr')
    ip_info_list = []
    for ip_info in ip_infos:
        info = ip_info.select('td')
        if info:
            ip_info_list.append({
                '代理IP地址': info[0].get_text(),
                '端口': info[1].get_text(),
                '服务器地址': info[2].get_text(),
                '是否匿名': info[3].get_text(),
                '类型': info[4].get_text(),
                '存活时间': info[5].get_text()
            })
    for item in ip_info_list:
        print(item)


"""
    2.网址：https://cs.lianjia.com/ershoufang/rs/
    
    用xpath做一个简单的爬虫，爬取链家网里的租房信息获取标题，位置，房屋的格局（三室一厅），关注人数，单价，总价    
"""


def zuoye2():
    url = 'https://cs.lianjia.com/ershoufang/rs/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49'
    }
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    house_list_data = html.xpath('//div[@class="info clear"]')
    house_info_list = []
    for house_info in house_list_data:
        # 用 if house_info: 控制台会报如下警告：
        # FutureWarning: The behavior of this method will change in future versions.
        # Use specific 'len(elem)' or 'elem is not None' test instead.
        if len(house_info):
            house_info_list.append({
                '标题': house_info.xpath('./div[@class="title"]/a/text()')[0],
                # '位置': '{}-{}'.format(
                #     house_info.xpath('.//div[@class="positionInfo"]/a/text()')[0],
                #     house_info.xpath('.//div[@class="positionInfo"]/a/text()')[1]
                # ),
                '位置': '-'.join(house_info.xpath('.//div[@class="positionInfo"]/a/text()')),
                '房屋格局': house_info.xpath('.//div[@class="houseInfo"]/text()')[0].split(' | ')[0],
                '关注人数': house_info.xpath('./div[@class="followInfo"]/text()')[0].split(' / ')[0],
                '单价': house_info.xpath('.//div[@class="unitPrice"]/span/text()')[0],
                '总价': house_info.xpath('.//div[@class="totalPrice totalPrice2"]/span/text()')[0] + '万'
            })
    for item in house_info_list:
        print(item)


def main():
    # 作业1
    print('=' * 20, '作业1', '=' * 20)
    zuoye1()

    # 作业2
    print('\r\n' * 2, '=' * 20, '作业2', '=' * 20)
    zuoye2()
    print('=' * 46)


if __name__ == '__main__':
    main()
