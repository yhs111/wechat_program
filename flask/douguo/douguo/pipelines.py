# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from bson import ObjectId
from settings import DB_MONGO

class DouguoPipeline(object):
    num = 1

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(DB_MONGO["host"], DB_MONGO["port"])
        self.db = self.client['toutiao']
        self.user = self.db.user_info
        self.index = self.db.user_id

    def process_item(self, item, spider):
        dic = dict(item)
        uid = self.user.insert(dic)
        self.index.insert({"uid": ObjectId(uid)})
        return item

    def close_spider(self, spider):
        self.client.close()
        self.num = None
