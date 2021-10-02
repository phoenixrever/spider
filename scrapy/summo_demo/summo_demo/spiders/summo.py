import time

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError

from summo_demo.items import SummoDemoItem

"""
todo summo qps 限制了  并发
"""


class SummoSpider(scrapy.Spider):
    name = 'summo'
    # allowed_domains = ['summo.com']
    # ct 房租上限
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }
    start_urls = [
        'https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0065&ek=006534520&cb=0.0&ct=5.0&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&po2=99&pc=10']
    url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0065&ek=006534520&cb=0.0&ct=5.0&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&po2=99&pc=10&page=%d'
    page_num = 2

    def parse(self, response):
        groups = response.xpath('//div[@class="property_group"]')
        for item in groups:
            # .// 表示当前节点下的元素
            names = item.xpath('.//*[@class="property_inner-title"]/a/text() ').extract()
            hrefs = item.xpath('.//a[@class="js-cassetLinkHref"]/@href').extract()
            # 详情页发送请求
            for i in range(0, len(hrefs)):
                url_detail = 'https://suumo.jp' + hrefs[i]
                # print(url_detail)
                item = SummoDemoItem()
                item['name'] = names[i]
                yield scrapy.Request(url=url_detail, callback=self.parse_detail,
                                     errback=self.errback_httpbin,
                                     # headers=self.headers,
                                     meta={
                                         'max_retry_times': 1,
                                         # 'handle_httpstatus_all': True
                                         'item': item  # item传递给detail
                                     })
            # print(names)
            # print(hrefs)
        if (self.page_num <= 5):
            page_url = format(self.url % self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse_detail(self, response):
        data = response.xpath('//*[@id="wrapper"]/div[3]/div[1]/h1/text()').extract()
        # 接受传过来的meta 函数
        item = response.meta['item']
        # 去掉\N \T
        item['detail'] = ''.join(data[0].split())
        print(item)

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        # if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        # elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        # elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
