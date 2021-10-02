# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeLine(ImagesPipeline):

    # 对item中的图片进行请求操作
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['src'])

    # 指定图片的名字
    # 存储路径在settings中指定
    def file_path(self, request, response=None, info=None, *, item=None):
        img_name=request.url.split("/")[-1]
        return img_name

    # return item 值会传递给下一个将要执行的管道类
    def item_completed(self, results, item, info):
        return item

# class ImagePipelinePipeline:
#     def process_item(self, item, spider):
#         return item
