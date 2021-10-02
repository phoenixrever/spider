# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlSpiderDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    href = scrapy.Field()

class DetailItem(scrapy.Item):
    title = scrapy.Field()