# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  企查查.py
# @Author  ：  jflmao
# @Time    ：  2023-06-18 13:50
# @Software：  PyCharm
# ==============================
import re

import execjs
import requests
from typing import Tuple


class QCC:
    def __init__(self, enterprise_id):
        self.sess = requests.Session()
        self.enterprise_id = enterprise_id
        self.cookie = ""  # 需要登录后的cookie
        self.headers = {
                "authority": "www.qcc.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "cache-control": "no-cache",
                "dnt": "1",
                "pragma": "no-cache",
                "referer": f"https://www.qcc.com/firm/{self.enterprise_id}.html",
                "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "cookie": self.cookie,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
            }
        self.data = {
            "keyNo": self.enterprise_id,
            "pageIndex": 2,  # 页码
            "pageSize": 10,
            "sortField": "",
            "isSortAsc": False
        }

    def get_pid_tid(self) -> Tuple[str, str]:
        """
            获取 Pid 和 Tid 的值

        :return: pid, tid
        """
        url = f"https://www.qcc.com/astock/{self.enterprise_id}.html"
        self.sess.headers = self.headers
        res = self.sess.get(url).text

        try:
            p = re.findall("pid='(.*?)'", res)[0]
            t = re.findall("tid='(.*?)'", res)[0]
        except:
            p = ''
            t = ''

        return p, t

    def get_info(self) -> None:
        """
            获取关联交易信息

        :return: 无
        """
        pid, tid = self.get_pid_tid()

        with open('加密逆向.js') as f:
            jstext = f.read()
        job = execjs.compile(jstext)
        Key = job.call('key', "/api/astock/relatedtradelist", self.data)
        value = job.call('value', "/api/astock/relatedtradelist", self.data, tid)
        self.sess.headers.update({
            Key: value,
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "origin": "https://www.qcc.com",
            "cookie": self.cookie,
            "x-pid": pid,
            "x-requested-with": "XMLHttpRequest"
        })
        url = "https://www.qcc.com/api/aStock/relatedTradeList"
        res = self.sess.post(url, json=self.data).json()
        for item in res['Result']:
            print('交易方：', item['RelatpartyName'], '  交易金额：', item['TransactionMoney'])


def main():
    enterprise_id = '5dffb644394922f9073544a08f38be9f'
    qcc = QCC(enterprise_id)
    qcc.get_info()


if __name__ == '__main__':
    main()
