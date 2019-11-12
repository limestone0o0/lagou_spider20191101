from scrapy import signals
from threading import Timer
import random
import requests
from lagouzhaopin.settings import LAHG, POSITION
from fake_useragent import UserAgent

class CookieDownloaderMiddleware(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/list_%s/p-city_%s?&cl=false&fromSearch=true&labelWords=&suginput='%(LAHG,POSITION)
        self.ua = UserAgent()
        self.head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': random.choice(self.ua.random),
            'Host': 'www.lagou.com',
        }
        self.proxys = [
            '101.132.42.164:5739', '39.137.69.9:8080', '106.14.222.15:5739', '139.159.225.81:9090',
            '58.248.62.137:8080','101.4.136.34:81','39.137.69.10:80','106.14.201.32:5739',
            '106.14.11.159:5739','111.29.3.193:8080','36.104.132.178:3128','62.210.124.248:3128'
]
        self.set_time()

    def get_cookie(self):
        session = requests.session()
        temp = random.choice(self.proxys)
        try:
            session.get(self.url, headers=self.head, proxies={'http': 'http://'+temp})
        except:
            self.proxys.remove(temp)
            temp = random.choice(self.proxys)
            session.get(self.url, headers=self.head, proxies={'http':  'http://'+temp})

        cookie = session.cookies.get_dict()
        return cookie

    def set_time(self):
        self.cookie = self.get_cookie()
        t = Timer(1, self.set_time)
        t.start()


    def process_request(self, request, spider):

        request.cookies = self.cookie
        # request.headers['User-Agent'] = random.choice(self.user_agent)
        request.headers['User-Agent'] = self.ua.random

        return None


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
