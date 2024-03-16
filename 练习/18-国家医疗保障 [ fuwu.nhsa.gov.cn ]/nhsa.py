# -*- coding: utf-8 -*-
# ==============================
# @Time    : 2024/3/14 23:00
# @File    : nhsa.py
# @Author  : jflmao
# @SoftWare: PyCharm
# ==============================

import execjs

with open('dec.js', 'r', encoding='utf-8', errors='ignore') as f:
    js_code = f.read()

ctx = execjs.compile(js_code)
ress = ctx.call('getReqData')
res = ctx.call('getDecDate')

print(res)
