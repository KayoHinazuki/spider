# encoding=utf-8
from cookie import cookies

class CookieMiddleware(object):
    def process_request(self, request, spider):
        cookie = cookies
        request.cookies = cookies