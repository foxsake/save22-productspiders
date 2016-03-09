# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

from productspiders.items import WwwExpansysComSgCrawlerItem
from productspiders.loader.www_expansys_com_sg_loader import WwwExpansysComSgLoader

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
                # print 'hell yea!--'
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
        # item = WwwExpansysComSgCrawlerItem()
        crawl_time = u'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        l = WwwExpansysComSgLoader(item = WwwExpansysComSgCrawlerItem(),response=response)

        l.add_value('crawl_time',crawl_time)
        l.add_value('url', unicode(response.url))

        l.add_xpath('retailer_sku_code','//@data-sku')

        l.add_xpath('title','//div[@id="title"]/h1/text()')
        l.add_xpath('title','//div[@id="title"]/h1/small/text()')

        l.add_xpath('brand','//*[@id="prod_core"]/ul/li[4]/a/text()')
        l.add_xpath('primary_image_url','//*[@id="image"]/a/@href')
        l.add_xpath('image_urls','//div[@class="product__gallery"]/ul/li/a/@href')
        l.add_xpath('currency','//*[@id="price"]/meta/@content')
        l.add_xpath('instock','//*[@id="stock"]/@content')

        l.add_xpath('current_price','//*[@id="price"]/strong/span/text()')
        l.add_xpath('current_price','//*[@id="price"]/strong/span/sup/text()')

        l.add_xpath('categories','//*[@id="breadcrumbs"]/li/a/span/text()')

        l.add_xpath('description','//*[@id="description"]')
        # l.add_xpath('rating','//*[@id="review_avg"]/span[1]/text()')
        
        # item['ean'] = response.xpath('//*[@id="prod_core"]/ul/li[2]/span/text()').extract()
        # item['mfr'] = response.xpath('//*[@id="prod_core"]/ul/li[3]/span/text()').extract()  

        # item['description'] = response.xpath('//div[@id="description"]/h2/text()').extract()

        # if response.xpath('//*[@id="prod_core"]/span/ul/li[1]/strong/strike'):
        #     item['price'] = response.xpath('//*[@id="prod_core"]/span/ul/li[1]/strong/strike/text()').extract()[0] + response.xpath('//*[@id="prod_core"]/span/ul/li/strong/strike/sup/text()').extract()[0] #if response.xpath('//*[@id="prod_core"]/span/ul/li/strong/strike') else item['current_price']
        # else:
        #     item['price'] = item['current_price']
        # print 'the price = ',item['price'],',current_price = ',item['current_price']
        
        return l.load_item()
