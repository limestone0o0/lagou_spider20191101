# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouzhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionId = scrapy.Field()  # 文章id
    art_title = scrapy.Field()
    art_time = scrapy.Field()
    art_position = scrapy.Field()
    art_salary = scrapy.Field()  # 工资
    art_work_year = scrapy.Field()  # 要求工作年限
    art_education = scrapy.Field()  # 学历要求
    art_jobNature = scrapy.Field()  # 职位类型全职
    company_hitags = scrapy.Field()  # 公司福利
    art_company_name = scrapy.Field()
    art_company_id = scrapy.Field()

    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_financestage = scrapy.Field()  # 公司融资轮数
    company_label_list = scrapy.Field()  # 公司吸引力
    art_first_type = scrapy.Field()  # 具体职位类型
    art_second_type = scrapy.Field()  # 总体职位类型
    art_third_type = scrapy.Field()  # 语言职位类型

    compangy_full_position = scrapy.Field()#具体位置
    art_description = scrapy.Field()
    fingerprint = scrapy.Field()
