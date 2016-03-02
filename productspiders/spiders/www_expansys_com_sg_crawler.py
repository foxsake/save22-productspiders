# -*- coding: utf-8 -*-
import scrapy


class WwwExpansysComSgCrawler(scrapy.Spider):
    name = "www_expansys_com_sg_crawler"
    allowed_domains = ["www.expansys.com.sg"]
    start_urls = (
        'http://www.www.expansys.com.sg/',
    )

    def parse(self, response):
        pass
