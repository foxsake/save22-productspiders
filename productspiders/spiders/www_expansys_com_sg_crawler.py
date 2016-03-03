# -*- coding: utf-8 -*-
import scrapy

from productspiders.items import ProductspidersItem

class WwwExpansysComSgCrawler(scrapy.Spider):
    name = "www_expansys_com_sg_crawler"
    allowed_domains = ["www.expansys.com.sg"]
    start_urls = (
        'http://www.expansys.com.sg/',
    )

    def parse(self, response):
        for ln in response.xpath('//*[@class="nitem"]/@href'):
            print ln
        # for pr in response.xpath('//*[@id="product"]'):
        #     item = ProductspidersItem()
        #     item["title"] = pr.xpath('//*[@id="title"]/h1/text()').extract()
        #     item["url"] = pr.xpath("a/@href").extract()
        #     yield item
        pass