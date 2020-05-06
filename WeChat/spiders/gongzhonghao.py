# -*- coding: utf-8 -*-
import os
import re
import random
import scrapy
import pandas as pd
import requests
from scrapy import Request
import pymongo
from WeChat.items import WechatItem
from scrapy.utils.project import get_project_settings

client = pymongo.MongoClient('127.0.0.1')
db = client['微信']
settings = get_project_settings()
cookie_url = settings.get("CookieUrl")

class GongzhonghaoSpider(scrapy.Spider):

    name = 'gongzhonghao'
    allowed_domains = ['mp.weixin.qq.com']

    def start_requests(self):
        data = db.baoxian.find(no_cursor_timeout=True)
        for i in data:
            url = i.get('url')
            category = i.get('category')
            PWeChatName = i.get('PWeChatName')
            token,cookie = self.token_cookies()
            detail_url = url.replace('token=%s','token=%s&'%token)
            yield Request(detail_url, cookies=cookie,
                          callback=self.parse_detail,
                          meta={'category': category, 'PWeChatName': PWeChatName,'url':url})
            
    def parse_detail(self,response):
        
        for i in eval(response.text).get('app_msg_list'):
            item = WechatItem()
            item['link'] = i.get('link')
            item['category'] = response.meta.get('category')
            item['PWeChatName'] = response.meta.get('PWeChatName')
            item['aid'] = i.get('aid')
            item['appmsgid'] = i.get('appmsgid')
            item['cover'] = i.get('cover')
            item['digest'] = i.get('digest')
            item['item_show_type'] = i.get('item_show_type')
            item['itemidx'] = i.get('itemidx')
            item['title'] = i.get('title')
            item['update_time'] = i.get('update_time')

            yield item
        db.baoxian.delete_one({"url":response.meta.get('url')})
        
    def token_cookies(self):
        data = requests.get(cookie_url).json()
        token = data.get('token')
        return token,data