# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class WechatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    aid = Field()
    appmsgid = Field()
    cover = Field()
    digest = Field()
    item_show_type = Field()
    itemidx = Field()
    link = Field()
    title = Field()
    update_time = Field()
    category = Field()
    PWeChatName= Field()

class UrlItem(scrapy.Item):

    url = Field()
    PWeChatName = Field()
    category = Field()