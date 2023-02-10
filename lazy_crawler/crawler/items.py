
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader

class ScrapingTestingLoader(ItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()