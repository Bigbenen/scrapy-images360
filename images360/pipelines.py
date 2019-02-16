# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings['MONGO_URI'],
            mongo_db = crawler.settings['MONGO_DB']
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings['MYSQL_HOST'],
            database = crawler.settings['MYSQL_DB'],
            user = crawler.settings['MYSQL_USER'],
            password = crawler.settings['MYSQL_PASSWORD'],
            port = crawler.settings['MYSQL_PORT']
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database,
                                  charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'insert into {} ({}) values ({})'.format(item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()

class ImagePipeline(ImagesPipeline):
    #首先要在settings.py定义存储路径
    #IMAGES_STORE

    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-1]
        return file_name

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['url'])

    def item_completed(self, results, item, info):
        #看results结构
        #print('\n',results)
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('Image Download Failed')
        return item

        # 上述筛选条件并不严格，在本例中可优化如下
        #上述条件严格，且适合每个item['url']对应多个下载对象的情况，更通用，不用优化。
        #ok,x = results[0]
        #if ok and x:
        #    return item
        #else:
        #    raise DropItem('\n###Image Download Failed###')