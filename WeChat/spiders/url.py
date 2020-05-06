# -*- coding: utf-8 -*-
import os
import re
import random
import scrapy
import pandas as pd
from scrapy import Request
import requests
from WeChat.items import WechatItem, UrlItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

file_path = settings.get("FilePath")
cookie_url = settings.get("CookieUrl")

class UrlSpider(scrapy.Spider):
    name = 'url'
    allowed_domains = ['mp.weixin.qq.com']

    def start_requests(self):
        global  index
        fileNames = os.listdir(file_path)
        fileNames = ['finance.xlsx']
        
        searchIdUrl = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token=%s&lang=zh_CN&f=json&ajax=1&query=%s&begin=0&count=10'

        for i in fileNames:
            if i.startswith('.'):
                continue
            data = pd.read_excel(file_path + i)
            for l_index,l in enumerate(data['关键词']):      
                token,cookie = self.token_cookies()
                yield Request(searchIdUrl % (token, l), cookies=cookie,
                              callback=self.parse_gongzhonghao, meta={'category': i.replace('.xlsx', ''),'count':data['top'][l_index]})

    def parse_gongzhonghao(self, response):

        article_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=%s&lang=zh_CN&f=json&ajax=1&action=list_ex&begin=0&count=5&query=&fakeid=%s&type=9'
        data = eval(response.text).get('list')
        count = response.meta.get('count')
        if not int(count):
            fakeid = data[0].get('fakeid')
            name = data[0].get('nickname')
            token,cookie = self.token_cookies()
            yield Request(article_url % (token, fakeid), cookies=cookie,callback=self.parse_detail,
                          meta={'category': response.meta.get('category'), 'name': name})

        else:
            if count > 10:
                count = 10
                
            for i in data[:count-1]:
                fakeid = i.get('fakeid')
                token,cookie = self.token_cookies()
                name = i.get('nickname')
                yield Request(article_url % (token, fakeid), cookies=cookie,
                              callback=self.parse_detail,
                          meta={'category': response.meta.get('category'), 'name': name})
                
                    
            if response.meta.get('count') > 10:
                
                url = response.url
                for l in range(10,response.meta.get('count'),10):
                    url = re.sub('begin=\d*','begin=%s'%l,url)
                    token,cookie = self.token_cookies()
                    url = re.sub('token=\d*','token=%s'%token,url)
                    yield Request(url,callback=self.parse_gongzhonghao,meta={'category':response.meta.get('category'),'count':response.meta.get('count')-10},cookies=cookie)


    def parse_detail(self, response):

        url = response.url
        url = re.sub('token=.*?&', 'token=%s', url)
        if not int(re.search('begin=(\d*)', url).group(1)):
            number_count = int(eval(response.text).get('app_msg_cnt'))
            for i in range(0, number_count, 5):
                url = re.sub('begin=\d*', 'begin=%s' % i, url)
                item = UrlItem()
                item['url'] = url
                item['category'] = response.meta.get('category')
                item['PWeChatName'] = response.meta.get('name')
                yield item

    def token_cookies(self):
        data = requests.get(cookie_url).json()
        token = data.get('token')
        return token,data
