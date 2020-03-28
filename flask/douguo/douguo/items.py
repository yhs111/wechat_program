# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DouguoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_url = scrapy.Field()
    classify = scrapy.Field()
    title = scrapy.Field()
    read_num = scrapy.Field()
    col_num = scrapy.Field()
    aut_img = scrapy.Field()
    aut_name = scrapy.Field()
    aut_desc = scrapy.Field()
    materials = scrapy.Field()
    step = scrapy.Field()
    tips = scrapy.Field()
    created_time = scrapy.Field()
