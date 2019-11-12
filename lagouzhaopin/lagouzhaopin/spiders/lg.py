# -*- coding: utf-8 -*-
import scrapy
import json
import re
import random
import logging
import hashlib
from lagouzhaopin.items import LagouzhaopinItem
from lagouzhaopin.settings import PAGE, LAHG, POSITION

logger = logging.getLogger(__name__)

class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['lagou.com']
    # start_urls = ['http://www.baidu.com']
    md5 = hashlib.md5()
    page = PAGE
    if page > 300:
        page = 300
    def start_requests(self):
        post_url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%s&needAddtionalResult=false'%str(POSITION)

        for i in range(1, self.page):
            formdata = {
                "first": "true",
                "pn": str(i),
                "kd": LAHG
            }
            yield scrapy.FormRequest(url=post_url, formdata=formdata, callback=self.parse)

    def deal_null(self, obj):
        if isinstance(obj, list):
            return ','.join(obj).strip()
        elif obj is None:
            return ''
        else:
            return obj

    def parse(self, response):
        item = LagouzhaopinItem()
        res_json_str = response.text
        res_json = json.loads(res_json_str)
        showId = res_json['content']['showId']#post请求id
        if res_json['content']['pageNo'] == '0':
            print('页数已经达到最大')
            return
        for i in res_json['content']['positionResult']['result']:
            try:
                item["positionId"] = i['positionId']#文章id
                item["art_title"] = i['positionName']
                item["art_time"] = i['createTime']
                item["art_position"] = i['district']
                item["art_salary"] = i['salary']#工资
                item["art_work_year"] = i['workYear']#要求工作年限
                item["art_education"] = i['education']#学历要求
                item["art_jobNature"] = i['jobNature']#职位类型全职
                item["company_hitags"] = self.deal_null(i['hitags'])#公司福利
                item["art_company_name"] = i['companyFullName']
                item["art_company_id"] = i['companyId']
                item["company_type"] = i['industryField']
                item["company_size"] = i['companySize']
                item["company_financestage"] = i['financeStage']#公司融资轮数
                item["company_label_list"] = self.deal_null(i['companyLabelList']) #公司吸引力
                item["art_first_type"] = i['firstType']#具体职位类型
                item["art_second_type"] = i['secondType']#总体职位类型
                item["art_third_type"] = i['thirdType']#语言职位类型
                uurl = 'https://www.lagou.com/jobs/%s.html?show=%s'%(i["positionId"],showId)
                self.md5.update(uurl.encode())
                item['fingerprint'] = self.md5.hexdigest()
                yield scrapy.Request(url=uurl, callback=self.next_parse,meta={'data': item} ,dont_filter=False)
            except Exception as e:
                self.logger.error(response.url)
                self.logger.error(e)
                continue

    def next_parse(self, response):
        item = response.meta['data']
        try:
            p = re.compile(r'.*<div class="job-detail">(.*)</div>\s+</dd>\s+<!-- Leader专访 -->.*', re.S)
            res2 = p.findall(response.text)
            item["art_description"] = self.deal_null(res2)
            temp = response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/text()').extract()
            item["compangy_full_position"] = self.deal_null(temp)
        except Exception as e:
            self.logger.error(str(response.url))
            self.logger.error(e)
        else:
            print(random.randint(0, 10))
        yield item
