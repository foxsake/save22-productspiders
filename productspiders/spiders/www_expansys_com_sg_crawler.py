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
            # print ln.extract()
            yield scrapy.Request(ln.extract(), callback=self.parse_nitem)
        # for pr in response.xpath('//*[@id="product"]'):
        #     item = ProductspidersItem()
        #     item["title"] = pr.xpath('//*[@id="title"]/h1/text()').extract()
        #     item["url"] = pr.xpath("a/@href").extract()
        #     yield item
    
    def parse_nitem(self,response):
        print 'looking in..'
        # for ln in response.xpath('//*[@id="product_listing"]/div/ul'):
        for ln in response.xpath('//*[@id="product_listing"]/div/ul/li[@class="title"]/h3/a/text()'):
            print ln.extract()
            # print ln.xpath('//*[@id="product_listing"]/div/ul/li[@class="title"]/h3/a/text()').extract()
            # print ln.xpath('//*[@id="product_listing"]/div/ul/li[@class="title"]/h3/a/@href').extract()
