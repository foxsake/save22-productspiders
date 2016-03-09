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
    return True if value.lower() == 'in_stock' else False

def get_rating(value):
    return (float(value) * 100) // 5.0


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

    rating_in = MapCompose(get_rating)
    rating_out = TakeFirst()



    

