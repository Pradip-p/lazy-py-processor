import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
from datetime import datetime

class LazyCrawler(LazyBaseCrawler):

    name = "support"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'RETRY_TIMES': 200,
        "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,
    }
    

    def start_requests(self): #project start from here.
        
        settings = get_project_settings()
        
        url = 'https://support.bpro.com.au/api/container'

        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        response = response.json()
        for res in response['containers']:
            for container in res['containers']:
                for articles in container.get('articles'):
                    _id = articles.get('id')
                    url = 'https://support.bpro.com.au/api/article/{}'.format(_id)
                    yield scrapy.Request(url, callback=self.get_details, dont_filter=True)

            for articles in res.get('articles'):
                _id = articles.get('id')

                url = 'https://support.bpro.com.au/api/article/{}'.format(_id)
                yield scrapy.Request(url, callback=self.get_details, dont_filter=True)

    def get_details(self, response):
        if response.text:
            response = response.json()
            article = response['article']
            #################
            categories = article['container'].get('name')
            dateCreated = article['dateCreated']
            dt = datetime.strptime(dateCreated, "%Y-%m-%dT%H:%M:%SZ")
            title = article['title']
            metaDescription = article['metaDescription']

            description = article['description']

            yield{
                'dateCreated': str(dt),
                'categories':categories,
                'title': title,
                'text': strip_html(description),
                # 'metaDescription':metaDescription,
            }
        else:
            print('*'*200)
        
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
