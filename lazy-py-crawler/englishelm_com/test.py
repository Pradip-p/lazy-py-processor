import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
import base64
from lazy_crawler.lib.user_agent import get_user_agent
import gc
from time import sleep

class LazyCrawler(LazyBaseCrawler):

    name = "englishelm"

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 32,'CONCURRENT_REQUESTS_PER_IP': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        # "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,
        'AUTO_THROTTLE':False,
        'RETRY_TIMES': 10,
        'ITEM_PIPELINES' :  {
        'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
        }
    }
    
    proxy = 'p.webshare.io:80'
    user_pass = base64.encodebytes("gkoffhkj-rotate:9qsx6zrpagq6".encode()).decode()

    # user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    page_number = 1

    def start_requests(self): #project start from here.

        url = 'https://englishelm.com/collections/all?page={}'.format(self.page_number)
        yield scrapy.Request(url, self.parse, dont_filter=True,
            meta={
                'proxy': 'http://' + self.proxy},
                headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
                'User-Agent': get_user_agent('random')
            }
            )

    def parse(self, response):
        gc.collect()
        urls = response.xpath('//div[@class="product-image image-swap"]/a[@class="product-grid-image"]/@href').extract()
        for _url in urls:
            url = 'https://englishelm.com{}{}'.format(_url,'.js')
            yield scrapy.Request(url, self.parse_details, dont_filter=True, 
            meta={
                'proxy': 'http://' + self.proxy,
            },
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            }
            )
    gc.collect()

    def parse_details(self, response):
        gc.collect()
        res = response.json()

        yield{
            'id': res['id'],
            'handle':res['handle'],
            'category': res['type'],
            'vendor':res['vendor'],
            'product_name': res['title'],
            'price': res['price'],
            'price_min':res['price_min'],
            'price_max':res['price_max'],
            'variants':str(res['variants']),
            'product_url': 'https://englishelm.com{}'.format(res['url']),
            'featured_image':'https:{}'.format(res['featured_image']),
            'image_url': ' | '.join(res['images']),
            'description': strip_html(str(res['description'])),
            'created_at':res['created_at'],
            'published_at':res['published_at']
        }
        self.page_number += 1
        # sleep(3)
        if self.page_number <= 17621:
            url = 'https://englishelm.com/collections/all?page={}'.format(self.page_number)
            yield scrapy.Request(url, self.parse, dont_filter=True,
            meta={
            'proxy': 'http://' + self.proxy,
            },
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            }
            )
        gc.collect()
    gc.collect()


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished