# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from productspiders.items import WwwExpansysComSgCrawlerItem
from productspiders.loader.www_expansys_com_sg_loader import WwwExpansysComSgLoader

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WwwExpansysComSgCrawler(CrawlSpider):
    name = "www_expansys_com_sg_crawler"
    allowed_domains = ["www.expansys.com.sg"]
    start_urls = (
        'http://www.expansys.com.sg/',
    )

    rules = (
        Rule(LinkExtractor(allow=(r'(.+)',),deny=(
            r'(.+)/contact_us(.+)?',
            r'(.+)/group(.+)?',
            r'(.+)/deal-of-the-day(.+)?',
            r'(.+)/business\+government(.+)?',
            r'(.+)/blog(.+)?',
            r'(.+)/forums(.+)?',
            r'(.+)/brands(.+)?',
            r'(.+)/public-relations(.+)?',
            r'(.+)/partnership-program(.+)?',
            r'(.+)/site-map(.+)?',
            r'(.+)/terms(.+)?',
            r'(.+)/my-account(.+)?',
            r'(.+)/order-tracking(.+)?',
            r'(.+)/delivery(.+)?',
            r'(.+)/top20(.+)?',
            r'(.+)/parrot-store(.+)?',
            r'(.+)/apple_store_asia(.+)?',
            r'(.+)/windows-8-landing(.+)?',
            r'(.+)/balckbery-store-asia(.+)?',
            r'(.+)/samsung-store(.+)?',
            r'(.+)/htc-store(.+)?',
            r'(.+)/sony-store(.+)?',
            r'(.+)/dji-store(.+)?',
            r'(.+)/parrot-store(.+)?',
            r'(.+)/nokia-store(.+)?',
            r'(.+)/yotaphone(.+)?',
            )),callback='parse_item',follow=True),
    )

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
        # l.add_xpath('currency','//*[@id="price"]/meta/@content')
        l.add_value('currency',unicode('SGD'))
        l.add_xpath('instock','//*[@id="stock"]/@content')

        l.add_xpath('current_price','//*[@id="price"]/strong/text()')
        l.add_xpath('current_price','//*[@id="price"]/strong/sup/text()')
        l.add_xpath('current_price','//*[@id="price"]/strong/span/text()')
        l.add_xpath('current_price','//*[@id="price"]/strong/span/sup/text()')
       
        l.add_xpath('categories','//*[@id="breadcrumbs"]/li/a/span/text()')

        l.add_xpath('description','//*[@id="description"]')
        
        l.add_xpath('rating','//*[@itemprop="average"]/text()')
        
        # item['ean'] = response.xpath('//*[@id="prod_core"]/ul/li[2]/span/text()').extract()
        # item['mfr'] = response.xpath('//*[@id="prod_core"]/ul/li[3]/span/text()').extract()  

        # if response.xpath('//*[@id="prod_core"]/span/ul/li[1]/strong/strike'):
        #     item['price'] = response.xpath('//*[@id="prod_core"]/span/ul/li[1]/strong/strike/text()').extract()[0] + response.xpath('//*[@id="prod_core"]/span/ul/li/strong/strike/sup/text()').extract()[0] #if response.xpath('//*[@id="prod_core"]/span/ul/li/strong/strike') else item['current_price']
        # else:
        #     item['price'] = item['current_price']
        # print 'the price = ',item['price'],',current_price = ',item['current_price']
        
        return l.load_item()
