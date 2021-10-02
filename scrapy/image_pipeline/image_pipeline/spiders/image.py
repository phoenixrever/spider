import scrapy
from image_pipeline.items import ImagePipelineItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    # allowed_domains = ['image.com']
    start_urls = ['https://javdb30.com/tags?c5=123&c10=1']

    def parse(self, response):
        item = ImagePipelineItem()
        imgs = response.xpath('//*[@id="videos"]//img/@data-src').extract()
        for img in imgs:
            item['src']=img
            print(img)
            yield item