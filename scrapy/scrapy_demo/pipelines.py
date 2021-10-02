# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ScrapyDemoPipeline:
    fp = None

    # 防止多次创建fp
    # open_spider 固定用法 要自定义函数需要在init定义具体见笔记
    def open_spider(self, spider):
        try:
            self.fp = open('scrapy_persistence.txt', 'w', encoding='utf-8')
        except Exception as e:
            print(e)

    # open_spider 固定用法
    def close_spider(self, spider):
        try:
            self.fp.close()
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        print(item)
        data_list = item['data_list']
        # 转为字符串存储
        self.fp.write(str(data_list))
        # 值传递给下一个管道类
        return item


# settings  ITEM_PIPELINES 中加上此类
class MysqlPipeline:
    conn = None
    cursor = None

    # open_spider 固定用法 要自定义函数需要在init定义具体见笔记
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='192.168.56.100', database='python', user='root', password='root',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    # open_spider 固定用法
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        data_list = item['data_list']
        # 注意python3中dict_keys(['data'])不允许切片，先转List再切片就好了
        for dic in data_list:
            keys = list(dic.keys())
            print(keys[0])
            print(dic["data"])
            try:
                self.cursor.execute(f' insert into scrapy(name,value) values("{keys[0]}","{dic["data"]}")')
                self.conn.commit()
            except Exception as e:
                print('error==>', e)
                self.conn.rollback()
        return item
