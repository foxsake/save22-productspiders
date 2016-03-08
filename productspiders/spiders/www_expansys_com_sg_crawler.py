# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

from productspiders.items import WwwExpansysComSgCrawlerItem

class WwwExpansysComSgCrawler(scrapy.Spider):
    name = "www_expansys_com_sg_crawler"
    allowed_domains = ["www.expansys.com.sg"]
    start_urls = (
        'http://www.expansys.com.sg/',
    )

    def parse(self, response):
        sgo = 'http://www.expansys.com.sg/smart-gadget-offers/'
        for ln in response.xpath('//*[@class="nitem"]/@href'):
            # print ln.extract()
            if ln.extract() == sgo:
                print 'hell yea!--'
                yield scrapy.Request(ln.extract(), callback=self.parse_sgo_link)
            else:
                yield scrapy.Request(ln.extract(), callback=self.parse_nitem)

    def parse_sgo_link(self,response):
        for nav in response.xpath('//*[@id="show_products"]/ul[2]/li/a/@href').extract():
            yield scrapy.Request(response.urljoin(nav),callback=self.parse_sgo)

    def parse_sgo(self, response):
        for itemLink in response.xpath('//*[@id="show_products"]/div/ul/li[2]/h3/a/@href').extract():
            yield scrapy.Request(response.urljoin(itemLink),callback=self.parse_item)
    
    def parse_nitem(self,response):
        # print 'looking in..'
        for ln in response.xpath('//*[@id="product_listing"]/div/ul/li[@class="title"]/h3/a/@href'):
            # print response.urljoin(ln.extract())
            yield scrapy.Request(response.urljoin(ln.extract()),callback=self.parse_item)

        another = response.xpath('//*[@id="footer_tools"]/ul/li/ul/li/a[@class="next"]/@href')
        if another:
            yield scrapy.Request(response.urljoin(another.extract()[0]), callback=self.parse_nitem)

    def parse_item(self,response):
        item = WwwExpansysComSgCrawlerItem()

        item['crawl_time'] = u'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

        item['url'] = response.xpath('//html/head/link[1]/@href').extract() 
        item['sku'] = response.xpath('//@data-sku').extract()  
        
        item['ean'] = response.xpath('//*[@id="prod_core"]/ul/li[2]/span/text()').extract()
        item['mfr'] = response.xpath('//*[@id="prod_core"]/ul/li[3]/span/text()').extract()  
        item['brand'] = response.xpath('//*[@id="prod_core"]/ul/li[4]/a/text()').extract() or None

        item['title'] = response.xpath('//div[@id="title"]/h1/text()').extract()
        item['description'] = response.xpath('//div[@id="description"]/h2/text()').extract()

        item['primary_image_url'] = response.xpath('//*[@id="image"]/a/@href').extract()
        item['image_urls'] = response.xpath('//div[@class="product__gallery"]/ul/li/a/@href').extract()

        item['currency'] = response.xpath('//*[@id="price"]/meta/@content').extract()
        item['current_price'] = (response.xpath('//p[@id="price"]/strong/span/text()').extract()[0] +
         response.xpath('//p[@id="price"]/strong/span/sup/text()').extract()[0] if response.xpath('//p[@id="price"]/strong/span/sup') else ''
         or None)
        if response.xpath('//*[@id="prod_core"]/span/ul/li[1]/strong/strike'):
            item['price'] = response.xpath('//*[@id="prod_core"]/span/ul/li[1]/strong/strike/text()').extract()[0] + response.xpath('//*[@id="prod_core"]/span/ul/li/strong/strike/sup/text()').extract()[0] #if response.xpath('//*[@id="prod_core"]/span/ul/li/strong/strike') else item['current_price']
        else:
            item['price'] = item['current_price']
        # print 'the price = ',item['price'],',current_price = ',item['current_price']
        item['instock'] = response.xpath('//*[@id="stock"]/@content').extract()
        yield item
