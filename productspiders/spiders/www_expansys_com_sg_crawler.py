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
    
    def parse_nitem(self,response):
        # print 'looking in..'
        for ln in response.xpath('//*[@id="product_listing"]/div/ul/li[@class="title"]/h3/a/@href'):
            # print response.urljoin(ln.extract())
            yield scrapy.Request(response.urljoin(ln.extract()),callback=self.parse_item)

        another = response.xpath('//*[@id="footer_tools"]/ul/li/ul/li/a[@class="next"]/@href')
        if another:
            yield scrapy.Request(response.urljoin(another.extract()[0]), callback=self.parse_nitem)

    def parse_item(self,response):
        item = ProductspidersItem()
        item['url'] = response.xpath('//html/head/link[1]/@href').extract() 
        item['sku'] = response.xpath('//@data-sku').extract()  
        item['ean'] = response.xpath('//*[@id="prod_core"]/ul/li[2]/span/text()').extract()
        item['brand'] = response.xpath('//*[@id="prod_core"]/ul/li[4]/a/text()').extract() or None
        item['title'] = response.xpath('//div[@id="title"]/h1/text()').extract()
        item['description'] = response.xpath('//div[@id="description"]/h2/text()').extract()
        item['image_urls'] = response.xpath('//*[@id="image"]/a/@href').extract()
        item['currency'] = response.xpath('//*[@id="price"]/meta/@content').extract()
        item['price'] = response.xpath('//p[@id="price"]/strong/span/text()').extract() + '.' + response.xpath('//p[@id="price"]/strong/span/sup/text()')
        yield item
