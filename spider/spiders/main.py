#encoding=utf-8
import re
from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.selector import Selector
from spider.items import UserItem, SenseItem
# from test2 import HTML
class WeiboSpider(CrawlSpider):
    name = 'weibo'
    host = 'weibo.cn'
    start_urls = ['http://weibo.cn/5842595131/follow']
    # start_urls = ['http://koily.com'] 
    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.filteUser)
        
    def filteUser(self, response):
        userItem = UserItem()
        selector = Selector(response)
        tables = selector.xpath('body/table')
        #提取userId  微博的图片地址换了 用不了了
        # def getUserId(string):
        #     try:            
        #         m = re.match('^.*?cn/(.*?)/.*?$', string)
        #         return m.group(1)
        #     except BaseException, e:
        #         print '获取userId错误: ', e
        #         print 'avatar URL: ', string 
           
        def isFriend(arr):
            if len(arr) == 1:
                return False
            else:
                return True
                
        for table in tables:
            # print table.xpath
            #用户uri
            # print table.xpath('tr/td[1]/a/@href').extract()[0]
            #用户昵称
            nickname = table.xpath('tr/td[2]/a/text()').extract()[0]
            userItem['nickname'] = nickname
            print nickname
            #avatar地址
            avatar = table.xpath('tr/td[1]/a/img/@src').extract()[0]
            userItem['avatar'] = avatar
            # print avatar
            # #userId
            # userId = getUserId(avatar)
            #是否关注
            isFollow = True
            userItem['isFollow'] = isFollow
            #是否相互关注
            userItem['isFriend'] = isFriend(table.xpath('tr/td[2]/text()').extract())
            _url = table.xpath('tr/td[2]/a/@href').extract()[0]
            yield Request(url=_url, meta={'userItem': userItem}, callback=self.filteSense)
    def filteSense(self, response):
        #获取userId
        def getUserId(string):
            m = re.match('/(.*?)/avatar', string)
            return m.group(1)
        # 获取weibo发布时间    
        def getTime(string):
            _minute = re.match(u'^(.*?)分钟前', string)
            _time = re.match(u'^.*?(\d{2}):(\d{2})', string)
            _today = re.match(u'今天', string)
            _toyear = re.match(u'(\d{2})月(\d{2})日', string)
            _date = re.match('(\d{4})-(\d{2})-(\d{2})', string)
            _now = datetime.now()
            now = datetime(_now.year, _now.month, _now.day, _now.hour, _now.minute)
            if _minute != None:
                time_delta = int(_minute.group(1))
                time = now - timedelta(minutes= time_delta)
                return time
            elif _today !=None:
                time_hour = int(_time.group(1))
                time_minute = int(_time.group(2))
                time = datetime(_now.year, _now.month, _now.day, time_hour, time_minute)
                return time  
            elif _toyear != None:
                time_month = int(_toyear.group(1))
                time_day = int(_toyear.group(2))
                time_hour = int(_time.group(1))
                time_minute = int(_time.group(2))
                time = datetime(_now.year, time_month, time_day, time_hour, time_minute)
                return time
            elif _date !=None:
                time_year = int(_date.group(1))
                time_month = int(_date.group(2))
                time_day = int(_date.group(3))
                time_hour = int(_time.group(1))
                time_minute = int(_time.group(2))        
                time = datetime(time_year, time_month, time_day, time_hour, time_minute)        
                return time  
        def getCommentId(string):
            m = re.match('^M_(.*?)$', string)
            commentId = m.group(1)
            return commentId                
        # print len(_senses)
        senseItem = SenseItem()
        selector = Selector(response)
        senses = selector.xpath('body/div[@class="c"]')  
        if 'userId' in response.meta:
            userId = response.meta['userId']
        else:        
            _userId = selector.xpath('body/div[@class="u"]/table/tr/td[1]/a/@href').extract()[0]
            print _userId
            userId = getUserId(_userId) 
        #userId
        print userId                        
        for sense in senses:
            # 发表的微博内容  
            # print _sense.css('.ctt::text').extract()[0]
            # 组图链接
            # print _sense.css('.ctt a').extract()
            if len(sense.css('.ct')) != 0:      
                time = getTime(sense.css('.ct::text').extract()[0])
                #发表时间
                print time
                senseItem['time'] = time
                #commentId
                commentId = getCommentId(sense.xpath('@id').extract()[0])
                print commentId
                senseItem['commentId'] = commentId
                senseItem['userId'] = userId
                yield senseItem             
        _next = selector.xpath(u'body/div[@id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if len(_next) != 0:
            nextUrl = 'http://' + self.host + _next[0]
            print nextUrl,'nexturl'
            yield Request(url=nextUrl, meta={'userId': userId},callback=self.filteSense)
        else:
            userItem = response.meta['userItem']    
            userItem['userId'] = userId 
            yield userItem                     