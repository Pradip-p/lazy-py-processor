import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
import base64
from lazy_crawler.lib.user_agent import get_user_agent
import gc

class LazyCrawler(LazyBaseCrawler):

    name = "englishelm"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 32,'CONCURRENT_REQUESTS_PER_IP': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,'RETRY_TIMES': 200,
        "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,
        'ITEM_PIPELINES' :  {
        'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
        }
    }
    

    proxy = 'p.webshare.io:80'
    user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    page_number = 1
    def start_requests(self): #project start from here.

        # urls = ['https://englishelm.com/collections/all']
        # for url in urls:
        url = 'https://englishelm.com/collections/all?page={}'.format(self.page_number)
        yield scrapy.Request(url, self.parse, dont_filter=True,
            meta={'proxy': 'http://' + self.proxy},
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            })

    def parse(self, response):
        urls = response.xpath('//div[@class="product-image image-swap"]/a[@class="product-grid-image"]/@href').extract()
        for _url in urls:
            url = 'https://englishelm.com{}{}'.format(_url,'.js')
            product_url = 'https://englishelm.com{}'.format(_url)
            yield scrapy.Request(url, self.parse_details, dont_filter=True, 
            meta={'proxy': 'http://' + self.proxy,
            'product_url':product_url,
            },
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            })

        # next_page = response.xpath('//ul[@class="pagination-page"]/li[@class="text"]/a[@title="Next"]/@href').extract_first()
        # # print(next_page)
        # if next_page:
        #     url = 'https://englishelm.com{}'.format(next_page)
        #     yield scrapy.Request(url, self.parse, dont_filter=True,
        #     meta={'proxy': 'http://' + self.proxy,
        #     },
        #     headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
        #     'User-Agent': get_user_agent('random')
        #     })
    def parse_details(self, response):
        res = response.json()
        # title = res['title']
        description = res['description']
        vendor = res['vendor']
        # _type = res['type']
        images = res['images']
        variants = res['variants']
        category = res['type']
        for variant in variants:
            created_at = ''
            updated_at = ''
            if variant['featured_image']:
                created_at = variant['featured_image'].get('created_at')
                updated_at = variant['featured_image'].get('updated_at')
                
            sku = variant['sku'].strip()
            image_url = []
            for image in images:
                if sku in image:
                    image = 'https:{}'.format(image)
                    image_url.append(image)
                else:
                    if sku.lower() in image:
                        image = 'https:{}'.format(image)
                        image_url.append(image)
            available = variant['available']
            if available:
                available = 'Yes'
            else:
                available = 'No'
            price = int(variant['price'])/100
            inventory_management = variant['inventory_management']
            name = variant['name']
            barcode = variant['barcode']
            colors = ''.join(variant['option1'])
            yield{
                'upc': barcode,
                'sku':sku,
                'category': category,
                'vendor':vendor,
                'product_name': name,
                'price': price,
                'product_url': response.meta['product_url'],
                'image_url': ' | '.join(image_url),
                'description': strip_html(str(description)),
                'available': available,
                'colors':colors,
                'inventory_management': inventory_management,
                'created_at':created_at,
                'updated_at':updated_at
            }
            self.page_number += 1
            if self.page_number <= 17621:
                url = 'https://englishelm.com/collections/all?page={}'.format(self.page_number)
                yield scrapy.Request(url, self.parse, dont_filter=True,
                meta={'proxy': 'http://' + self.proxy,
                },
                headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
                'User-Agent': get_user_agent('random')
                })
            gc.collect()


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished