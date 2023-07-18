# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  有道翻译.py
# @Author  ：  jflmao
# @Time    ：  2023-07-18 14:29
# @Software：  PyCharm
# ==============================
import hashlib
import json
import time

import execjs
from requests import Session, utils


# noinspection NonAsciiCharacters
class LANG:
    AUTO = "auto"
    中文 = "zh_CHS"
    英语 = "en"
    日语 = "ja"
    韩语 = "ko"
    法语 = "fr"
    默认 = ""


class YOUDAO(object):
    def __init__(self):
        self.data = None
        self.url = "https://dict.youdao.com/webtranslate/key"
        self.sess = Session()
        cookies = "OUTFOX_SEARCH_USER_ID_NCOO=1393269207.1100566; OUTFOX_SEARCH_USER_ID=727599050@218.22.69.126"
        # noinspection PyTypeChecker
        cookies_dict = dict([ck.strip().split("=") for ck in cookies.split(";")])
        self.sess.cookies = utils.cookiejar_from_dict(cookies_dict)
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Origin": "https://fanyi.youdao.com",
            "Pragma": "no-cache",
            "Referer": "https://fanyi.youdao.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.params = {}
        with open('加解密.js') as f:
            jstext = f.read()
        self.job = execjs.compile(jstext)
        self.secretKey = None

    @staticmethod
    def get_sign(nowtime, key) -> str:
        """
            获取 签名 的 MD5 hash字符串
        :param nowtime: 时间戳
        :param key: key值
        :return: 返回 签名的 MD5 hash字符串
        """
        args = 'client=fanyideskweb&mysticTime={}&product=webfanyi&key={}'.format(nowtime, key)
        return hashlib.md5(args.encode("utf-8")).hexdigest()

    def get_secretKey(self) -> str:
        """
            获取 secretKey 字符串
        :return: 返回获取的 secretKey 字符串
        """
        mysticTime = str(int(time.time() * 1000))
        self.sess.headers = self.headers
        self.params = {
            "keyid": "webfanyi-key-getter",
            "sign": self.get_sign(mysticTime, "asdjnjfenknafdfsdfsd"),
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": mysticTime,
            "keyfrom": "fanyi.web"
        }
        res = self.sess.get(self.url, params=self.params).json()
        return res['data']['secretKey']

    def translate(self, i: str, source: str = LANG.AUTO, to: str = LANG.默认) -> str:
        """
            翻译主方法，默认中文翻译成英文，英文翻译成中文
        :param i: 需要翻译的字符串
        :param source: 需要翻译的字符串的语言，默认自动
        :param to: 翻译后的语言，默认自动
        :return: 返回翻译后的字符串
        """
        nowtime = str(int(time.time() * 1000))
        if not self.secretKey:
            self.secretKey = self.get_secretKey()
        self.sess.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "dict.youdao.com"
        })
        self.data = {
            "i": i,
            "from": source,
            "to": to,
            "dictResult": "true",
            "keyid": "webfanyi",
            "sign": self.get_sign(nowtime, self.secretKey),
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": nowtime,
            "keyfrom": "fanyi.web"
        }
        url = "https://dict.youdao.com/webtranslate"
        res = self.sess.post(url, headers=self.headers, data=self.data)
        return json.loads(self.job.call('get_decrypt', res.text))['translateResult'][0][0]['tgt']


if __name__ == '__main__':
    youdao = YOUDAO()
    print(youdao.translate("hello"))
