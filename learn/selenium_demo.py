# coding: utf-8
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver import ActionChains
from PIL import Image  ##调用库，包含图像类

options = webdriver.ChromeOptions()
# 不打开浏览器
# options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错

# 不加载图片
# options.add_argument('--blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
# 伪造请求 防止selenium 被监测到
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止网站识别Selenium代码

# 实例化一个浏览器对象
browser = webdriver.Chrome(executable_path='../scrapy/middleware_demo/middleware_demo/chromedriver.exe', options=options)

browser.get('https://javdb30.com/tags?c5=123&c10=1')
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[1]/div[2]/footer/a[1]').click()
# 搜索框中输入字符串
browser.find_element_by_id('video-search').send_keys('三宮つばき')
browser.find_element_by_id('search-submit').click()
# 必须等元素加载完成
# time.sleep(1)
# window.scrollTo(0,document.getElementById(".yall-loaded")) y 也可以是数字
# position = browser.find_element_by_xpath('//*[@id="videos"]/div/div[15]/a').location
# 窗口大小变化都会影响这个滚动  并不靠谱
# print(position)
# 滚动到目标
# browser.execute_script(f'window.scrollTo({position["x"]},{position["y"]})')
#截图
time.sleep(1)
browser.save_screenshot("screen_shoot.png")
# 获取imag 标签左上角位置信息
img = browser.find_element_by_xpath('//*[@id="videos"]/div/div[8]/a/div[1]/img')
location = img.location
size = img.size
rangle=([location['x'],location['y'],location['x']+size['width'],location['y']+size['height']])
print(rangle)
#crop
i = Image.open("screen_shoot.png")
frame = i.crop(rangle)
frame.save("pic.png")
# 拿到网页html
page_text = browser.page_source
tree = etree.HTML(page_text)
title = tree.xpath('//*[@id="videos"]/div/div[19]/a/div[3]/text()')
print(title)
# 切换浏览器标签定位的作用域
# browser.switch_to.frame('iframeId')
# action= ActionChains(browser)
# action.click_and_hold(browser.find_element_by_id('search-submit'))
# action.move_by_offset(100,0).perform()
# action.release()

time.sleep(5)
# browser.quit()
