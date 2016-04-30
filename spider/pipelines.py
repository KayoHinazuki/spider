# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis

class redisPipe(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379)
        print "pppppp"
        self.r.set('lsl','hahaha')
    def process_item(self, item, spider):
        print "哈哈哈哈"
        self.r.set('liyu','hahaha')
        return item
