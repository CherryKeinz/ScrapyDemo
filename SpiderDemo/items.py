# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderdemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class demoItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()

