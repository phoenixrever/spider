import scrapy
from selenium import webdriver

class MiddleSpider(scrapy.Spider):
    name = 'middle'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://news.163.com/']
    url='https://news.163.com/special/new2016_rshanghai_api/'

    #实例化一个浏览器对象供中间件response 调用
    def __init__(self, name=None, **kwargs):
        self.browser=webdriver.Chrome(executable_path="N:\python\scrapy\middleware_demo\middleware_demo\chromedriver.exe")

    def parse(self, response):
        # page_text= response.text
        # with open('baidu.html','w',encoding='utf-8') as fp:
        #     fp.write(page_text)
        yield scrapy.Request(url=self.url,callback=self.parse_detail)

    def parse_detail(self,response):
        print(response.text)
