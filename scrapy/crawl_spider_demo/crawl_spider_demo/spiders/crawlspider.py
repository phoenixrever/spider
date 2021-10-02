from redis import Redis
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawl_spider_demo.items import CrawlSpiderDemoItem

from crawl_spider_demo.items import DetailItem


class CrawlspiderSpider(CrawlSpider):
    name = 'crawlspider'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://news.yahoo.co.jp/topics/domestic']

    """
        LinkExtractor  提取符合allow正则指定的路径
        follow  true 爬取没有显示的页码 false  只爬取本页的
        链接提取器 继续作用到链接提取器提取到的链接
        2个链接提取器 随机允许的 没有id之类的标识符 无法保证插入数据库的对应
    """
    rules = (
        Rule(LinkExtractor(allow=r'topics/domestic(\?page=\d)+'), callback='parse_item', follow=True),
        # detail
        Rule(LinkExtractor(allow=r'pickup/\d+'), callback='parse_detail', follow=False),
    )

    # redis
    conn= Redis(host='192.168.56.100')

    # get() 返回str   extract() 返回[]
    def parse_item(self, response):
        item = CrawlSpiderDemoItem()
        lis = response.xpath('//*[@id="contentsWrap"]/div/div[3]/ul/li')
        for li in lis:
            name = li.xpath('.//div[@class="newsFeed_item_title"]/text()').get()
            date = li.xpath('.//time/text()').get()
            href = li.xpath('./a/@href').get()
            # 增量 set 检查重复的值 0 add失败说明存在
            result = self.conn.sadd('href',href)
            if(result ==0):
                break
            # print("name====>", name)
            # if(name!=None):
            item['name'] = name
            # if(date!=None):
            item['date'] = date
            item['href'] = href
        yield item

    def parse_detail(self, response):
        detialItem = DetailItem()
        title = response.xpath('//*[@id="uamods-pickup"]/div[2]/a/p/text()').get()
        # print("title====>", title)
        detialItem['title'] = title
        yield detialItem
