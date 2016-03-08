from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose


class WwwExpansysComSgLoader(ItemLoader):
    #TODO