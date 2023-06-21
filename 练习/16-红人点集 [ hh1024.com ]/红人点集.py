# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  红人点集.py
# @Author  ：  jflmao
# @Time    ：  2023-06-21 18:24
# @Software：  PyCharm
# ==============================
import time

import execjs
import requests

userphone = ''  # 手机号
password = ''  # 密码明文

with open('加密逆向.js', encoding='utf-8') as f:
    jstext = f.read()
job = execjs.compile(jstext)

pwd = job.call('get_pwd', password)  # 加密密码（MD5）
t = int(round(time.time() * 1000))
e = {
    "phoneNum": userphone,
    "pwd": pwd,
    "t": t,
    "tenant": 1
}
sig = job.call("get_sig", e)  # 加密参数（MD5）

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "DNT": "1",
    "Origin": "http://www.hh1024.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

url = "https://user.hrdjyun.com/wechat/phonePwdLogin"
e.update({'sig': sig})

token = requests.post(url, headers=headers, json=e).json()['data']['token']
print(token)
