import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import ipdb
from lazy_crawler.lib.html import to_browser


class LazyCrawler(LazyBaseCrawler):

    name = "primsrl"

    custom_settings = {
        'DOWNLOAD_DELAY': 0,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES' : {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
            }
        }
        
    page_num = 1

    def start_requests(self): #project start from here.
        
        settings = get_project_settings()
        url = 'https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/eng-gb/records?keyword=hoodie&page={}&urlCode=null&filter=sku'.format(self.page_num)
        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        data = response.json()
        brand  = 'Louis Vuitton'
        for data in data['skus']['hits']:
            link = data['url']
            product = data['name']
            price = data['offers']['priceSpecification'][0].get('price')
            category = data['category']
            gender = category[0][0]['name']

            # print(gender)
            yield {
                "brand": brand,
                "gender": gender,
                "product": product,
                "link": link,
                "price old" : '',
                'price_final': price
            }
        self.page_num += 1
        if self.page_num <= 3:
            url = 'https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/eng-gb/records?keyword=hoodie&page={}&urlCode=null&filter=sku'.format(self.page_num)
            yield scrapy.Request(url, self.parse, dont_filter=True)

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
settings = get_project_settings()
settings.setdict({
                'LOG_LEVEL': 'ERROR',
                'LOG_ENABLED': True,
            })
process = CrawlerProcess(settings)  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
