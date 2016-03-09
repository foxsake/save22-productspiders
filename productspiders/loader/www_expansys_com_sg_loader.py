from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose

import re

def parse_price(value):
    price = re.search(r'SG\$(\d+)',value)
    if price:
        return price.group(1)
    else:
        return value

def get_stock(value):
    return True if value == 'in_stock' else False

class WwwExpansysComSgLoader(ItemLoader):

    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = Join()

    image_urls_in = Identity()
    image_urls_out = Identity()

    categories_in = Identity()
    categories_out = MapCompose(unicode.strip)

    current_price_in = MapCompose(parse_price)
    current_price_out = Join(u'')

    instock_in = MapCompose(get_stock)
    instock_out = TakeFirst()

    description_in = Identity()
    description_out = Join()



    

