
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import logging
import yaml

# from lazy_crawler.puppeteer.puppeteer import browse
class LazyCrawler(LazyBaseCrawler):

    page_number = 1

    logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
    )
    
    custom_settings = {
        'DOWNLOAD_DELAY': 4,'RANDOMIZE_DOWNLOAD_DELAY':False,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls', 'RETRY_TIMES': 4, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
    }

    name = "amazon"

    settings = get_project_settings()

    settings.set('LOG_FILE','Log.log',priority='cmdline')
        
    def start_requests(self): #project start from here.
        
        # for url in urls:
        url = 'https://www.amazon.com/s?k=Electronics'
        yield scrapy.Request(url, self.parse_get_product_urls, dont_filter=True)



    def parse_get_product_urls(self, response):
        # asins = response.xpath('//span[@class="a-declarative"]/@data-s-easy-mode-ingress-button').extract()
        asins = response.xpath('//div[@data-component-type="s-search-result"]/@data-asin').extract()
        for asin in asins:
            # asin = yaml.load(asin).get('asin')
            url = f"https://www.amazon.com/dp/{asin}/"

            yield scrapy.Request(url, self.get_product_details, dont_filter=True,)


    def get_product_details(self, response):
        rating = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract_first()
        title = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        if title:
            title = title.strip()
        else:
            title = ''

        yield{
            'title':title,
            'Rating':rating,
        }

        if self.page_number <=20:
            self.page_number += 1
            url = f"https://www.amazon.com/s?k=Electronics&page={self.page_number}"
            yield scrapy.Request(url, self.parse_get_product_urls, dont_filter=True, )
    


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
