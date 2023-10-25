"""
    1.手写或者用工具画爬虫得采集流程
    ┌─────────→ 获取资源网址
    │               ↓
    │       发送请求获取响应数据
    │               ↓
    │           提取数据
    │               ↓
    └─────否─── 是否想要的数据
                    ↓ 是
                保存数据
"""
"""
    2.实战socket编程程序下载以下图片数据

    https://pic.netbian.com/uploads/allimg/220211/004115-1644511275bc26.jpg 
    https://pic.netbian.com/uploads/allimg/220215/233510-16449393101c46.jpg 
    https://pic.netbian.com/uploads/allimg/211120/005250-1637340770807b.jpg
"""

import socket
import re

urls = [
    'https://pic.netbian.com/uploads/allimg/220211/004115-1644511275bc26.jpg',
    'https://pic.netbian.com/uploads/allimg/220215/233510-16449393101c46.jpg',
    'https://pic.netbian.com/uploads/allimg/211120/005250-1637340770807b.jpg'
]


def get_image(url: str):
    res = b''
    host = url.split('/')[2]
    image_name = url.split('/')[-1]
    client = socket.socket()
    client.connect((host, 80))
    req = \
        f'GET {url} HTTP/1.0\r\n' \
        f'host: {host}\r\n' \
        'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
        '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49\r\n\r\n'
    client.send(req.encode())
    data = client.recv(1024)
    while data:
        res += data
        data = client.recv(1024)

    image = re.findall(b'\r\n\r\n(.*)', res, re.S)[0]

    with open(image_name, 'wb') as f:
        f.write(image)


if __name__ == '__main__':
    for item in urls:
        get_image(item)
