# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field

class SpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class UserItem(Item):
    '''
    头像地址 str
    userID str
    昵称    str
    是否关注 Boolean
    是否好友 Boolean 判断是否互相关注   
    #查看次数 int
    #关注时间 dateTime
    #time_to_know DataTime
    '''
    avatar = Field()
    userId = Field()
    nickname = Field()
    isFollow = Field()
    isFriend = Field()
    # pv = Field(Integer)
    # time_to_fellow = Field()
    # time_to_know = Field()   

class SenseItem(Item):
    '''
    ID  str （没懂这是什么ID）
    内容 str
    用户ID str
    微博ID str
    url  str  (没懂这是什么url)
    图片地址 （图片不止一张 所以这有问题）
    time (发表时间)
    '''
    # id = Field()
    # comment = Field()
    userId = Field()
    commentId = Field()
    # url = Field()
    # images=Field()
    time = Field()
    