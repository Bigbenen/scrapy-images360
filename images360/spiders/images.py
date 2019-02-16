# -*- coding: utf-8 -*-
import scrapy
from ..items import ImageItem
from urllib.parse import urlencode
import json

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://image.so.com/']

    #重写此方法，实际上start_ruls已经忽略
    def start_requests(self):
        base_url = 'http://image.so.com/zj?'
        data = {
            'ch': 'photography',
            'listtype': 'new',
            'temp': 1
        }
        for page in range(1, self.settings['MAX_PAGE'] + 1):
            data['sn'] = page * 30
            url = base_url + urlencode(data)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['title'] = image.get('group_title')
            item['url'] = image.get('qhimg_url')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item