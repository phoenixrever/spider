import scrapy
from scrapy.items import ScrapyDemoItem
from scrapy.http.request import Request


class DontcrySpider(scrapy.Spider):
    name = 'dontcry'  # 爬虫源文件的唯一标识
    # 允许start_urls 中哪些域名
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://javdb30.com']
    url = 'https://javdb30.com/?page=%d'
    page_num = 2
    data_list=[]

    # response 响应对象
    def parse(self, response):
        # extract 提取selector data  extract_first
        # ''.join(list) 列表转成字符串
        text = response.xpath('//*[@id="videos"]/div/div[40]/a/div[3]/text()')[0].extract()
        # text2 = ''.join(response.xpath('//*[@id="post-434795"]/div[1]/figure/a/@title').extract())
        # print(text)
        # print(text2)
        dic={
            'data':text
        }
        self.data_list.append(dic)
        if (self.page_num <=3):
            page_url = format(self.url % self.page_num)
            self.page_num += 1
            yield Request(url=page_url, callback=self.parse)
        print(self.data_list)
        # 增加返回值 以 -o 存入文件
        # return dic

        # 管道存储文件 导入管道类和items类
        # 实例化item对象
        item = ScrapyDemoItem()
        item['data_list'] = self.data_list
        # 将item 提交给管道
        yield item
