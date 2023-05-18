"""
目标网址：https://www.qqtxt.cc/list/1_1.html

通过正则获取到当前网页上更新列表里的所有小说名字(10页)
"""
import re

import requests


def get_xiaoshuo_name(_page: int) -> tuple:
    """
        获取指定页数的小说名字

    :param _page: 指定的页数
    :return: 返回小说名字的元组形式
    """
    url = f'https://www.qqtxt.cc/list/1_{_page}.html'
    response = requests.get(url)
    # response.encoding = 'gbk'
    response.encoding = response.apparent_encoding
    name_list = re.findall('target="_blank">(.*?)</a>》', response.text)
    return tuple(name_list)


def main():
    # 需要获取的总页数
    pages = 10
    # 计数器
    index = 0
    for page in range(1, pages + 1):
        for name in get_xiaoshuo_name(page):
            index += 1
            print(index, name)


if __name__ == '__main__':
    main()
