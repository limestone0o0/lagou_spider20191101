# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from lagouzhaopin.settings import LAHG

class LagouzhaopinPipeline(object):
    def __init__(self):
        myclient = pymongo.MongoClient(host="localhost", port=27017)
        self.db = myclient["test"]
        self.dbm = self.db[LAHG]


    def process_item(self, item, spider):
        self.dbm.insert(dict(item))

        return item
