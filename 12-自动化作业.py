# ==============================
# _*_ ending: utf-8 _*_
# ==============================
# @File    ：  12-自动化作业.py
# @Author  ：  jflmao
# @Time    ：  2023-01-31 13:40
# @Software：  PyCharm
# ==============================
"""
    地址：https://category.vip.com/suggest.php?keyword=%E5%8F%A3%E7%BA%A2&ff=235|12|1|1
    技术：selenium自动化
    字段：价格、标题 可以自行拓展
    保存：mongo
    交付：数据入库截图
"""
import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class VIP:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.collection = client['VIP']['shang_pin']
        # 配置选项
        options = webdriver.EdgeOptions()
        # 绕过检测
        options.add_argument('--disable-blink-features=AutomationControlled')
        # 不自动关闭
        options.add_experimental_option('detach', True)
        # 隐藏"Chrome正在受到自动软件的控制"
        options.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.browser = webdriver.Edge(options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.url = 'https://category.vip.com/suggest.php'

    def main(self):
        self.browser.get(self.url)
        s = self.browser.find_element(By.CLASS_NAME, 'c-search-input.J-search-input')
        s.send_keys('口红')
        time.sleep(1)
        s.send_keys(Keys.ENTER)
        self.get_info()

    def get_info(self):
        info_list = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c-goods-item.J-goods-item.c-goods-item--auto-width')))
        for item in info_list:
            items = {
                '标题': item.find_element(By.CLASS_NAME, 'c-goods-item__name').text,
                '价格': item.find_element(By.CLASS_NAME, 'c-goods-item__sale-price').text,
                '详情页': item.find_element(By.XPATH, './a[1]').get_attribute('href')
            }
            self.collection.insert_one(items)


if __name__ == '__main__':
    vip = VIP()
    vip.main()
    vip.browser.quit()
