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

from lxml import etree
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class VIP:
    def __init__(self):
        """
            初始化
        """
        self.client = MongoClient('localhost', 27017)
        self.collection = self.client['VIP']['shang_pin']
        # 删除集合
        # self.collection.drop()
        # 配置选项
        options = webdriver.EdgeOptions()
        # 绕过检测
        options.add_argument('--disable-blink-features=AutomationControlled')
        # 不自动关闭
        options.add_experimental_option('detach', True)
        # 隐藏"Chrome正在受到自动软件的控制"
        options.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 无头模式 在后台运行
        options.add_argument("-headless")
        # 禁止加载图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        self.browser = webdriver.Edge(options=options)
        self.url = 'https://category.vip.com/suggest.php?keyword=%E5%8F%A3%E7%BA%A2&ff=235|12|1|1'
        self.num = 0

    def main(self) -> None:
        """
            主方法

        :return: None
        """
        self.browser.get(self.url)
        # 统计页数
        page = 0
        while True:
            try:
                # 查找是否弹出登录 iframe
                login_iframe = self.browser.find_element(By.CLASS_NAME, 'login_iframe')
                print('登录窗口弹出了..')
                # 找到后就切换进去
                self.browser.switch_to.frame(login_iframe)
                # 找到关闭按钮并点击
                self.browser.find_element(By.CLASS_NAME, 'ui-dialog-close.vipFont.J-login-frame-close').click()
                # if login_close.is_enabled():
                #
                # login_close.click()
                print('已点击关闭按钮')
                # 切换回主文档
                self.browser.switch_to.default_content()
            except NoSuchElementException:
                pass
            self.parse_and_save_data(self.browser.page_source)
            page += 1
            print('获取第 {} 页源码完成..'.format(page))
            try:
                # 查找 下一页 按钮
                next_btm = self.browser.find_element(By.ID, 'J_nextPage_link')
            except NoSuchElementException:
                print('没有下一页了..')
                break
            else:
                # 找到后就点击下一页按钮
                next_btm.click()
        self.client.close()
        self.browser.quit()

    def parse_and_save_data(self, page_source: str) -> None:
        """
            解析并保存数据

        :param page_source: 网页源文件
        :return: None
        """
        html = etree.HTML(page_source)
        info_list = html.xpath('//div[@class="c-goods-item  J-goods-item c-goods-item--auto-width"]')
        for item in info_list:
            items = {
                '标题': item.xpath('.//div[@class="c-goods-item__name  c-goods-item__name--two-line"]/text()')[0] if
                len(item.xpath('.//div[@class="c-goods-item__name  c-goods-item__name--two-line"]/text()')) > 0 else
                item.xpath('.//div[@class="c-goods-item__name  c-goods-item__name--one-line"]/text()')[0],
                '现价': item.xpath('.//div[@class="c-goods-item__sale-price J-goods-item__sale-price"]/text()')[0],
                '原价': item.xpath('.//div[@class="c-goods-item__market-price  J-goods-item__market-price"]/text()')[0] if
                len(item.xpath('.//div[@class="c-goods-item__market-price  J-goods-item__market-price"]/text()')) > 0 else '无',
                '折扣': item.xpath('.//div[@class="c-goods-item__discount  J-goods-item__discount"]/text()')[0] if
                len(item.xpath('.//div[@class="c-goods-item__discount  J-goods-item__discount"]/text()')) > 0 else '无',
                '详情页': 'https:{}'.format(item.xpath('./a/@href')[0])
            }
            # 保存到MongoDB数据库
            self.collection.insert_one(items)
            self.num += 1
            print('第 {} 条数据保存完成..'.format(self.num))


if __name__ == '__main__':
    """
        脚本入口
    """
    t1 = time.time()
    vip = VIP()
    vip.main()
    print('用时：{} 秒'.format(time.time() - t1))
