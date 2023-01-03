import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import ipdb


class LazyCrawler(LazyBaseCrawler):

    name = "laptop"

    custom_settings = {
        'DOWNLOAD_DELAY': 0,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES' : {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
            }
        }
        
    

    def start_requests(self): #project start from here.
        
        settings = get_project_settings()
        blog_url = ['https://latop10.it/abbigliamento-moda/','https://latop10.it/auto/','https://latop10.it/musica/','https://latop10.it/prima-infanzia/',
        'https://latop10.it/regali/']

        blog = ['https://latop10.it/cucina-blog/','https://latop10.it/casa-blog/',
        'https://latop10.it/elettronica-blog/','https://latop10.it/prima-infanzia-blog/','https://latop10.it/prima-infanzia-blog/']

        urls = ['https://latop10.it/elettronica/','https://latop10.it/casa/','https://latop10.it/cucina/',
        'https://latop10.it/bellezza/','https://latop10.it/cura-della-persona/','https://latop10.it/salute/','https://latop10.it/sport/',
        'https://latop10.it/tempo-libero/','https://latop10.it/animali/','https://latop10.it/cibo-bevande/','https://latop10.it/fai-da-te/',
        'https://latop10.it/giardino/','https://latop10.it/fai-da-te/']

        urls.extend(blog_url)

        # url = 'https://latop10.it/elettronica/'
        for url in urls:
            
            # url = 'https://latop10.it/elettronica/antenna-Ricevitore-TV/' #not found
            yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        
        # uel = https://latop10.it/elettronica/proiettore/
        main_categories_urls = response.xpath('//div[@class="su-row"]/div[@class="su-column su-column-size-1-3"]/div[@class="su-column-inner su-u-clearfix su-u-trim"]/p/a/@href').extract()
        main_categories_name = response.xpath('//main[@class="content"]/div[@class="archive-description taxonomy-archive-description taxonomy-description"]/h1[@class="archive-title"]/text()').extract_first()
        for url in main_categories_urls:
        # url = 'https://latop10.it/elettronica/proiettore/'
            yield scrapy.Request(url, self.parse_get_sub_categories, dont_filter=True, meta={'main_categories_name':main_categories_name})


    def parse_get_sub_categories(self, response):
        sub_categories_name = response.xpath('//main[@id="genesis-content"]/div[@class="archive-description taxonomy-archive-description taxonomy-description"]/h1[@class="archive-title"]/text()').extract_first()
        sub_categories_urls = response.xpath('//main[@id="genesis-content"]/article/header[@class="entry-header"]/h2[@class="entry-title"]/a[@class="entry-title-link"]/@href').extract()
        # sub_categories_urls= response.xpath('//div[@class="su-row"]/div/div/p/a/@href').extract()

        for url in sub_categories_urls:
        # url = 'https://latop10.it/migliori-proiettori/'
            yield scrapy.Request(url, self.get_product_details, dont_filter=True, meta={'main_categories_name':response.meta['main_categories_name'], 'sub_categories_name':sub_categories_name})

    def get_product_details(self, response):
        main_categories_name = response.meta['main_categories_name']
        sub_categories_name = response.meta['sub_categories_name']
        product_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//main[@id="genesis-content"]/article/header[@class="entry-header"]/h1[@class="entry-title"]/text()').extract_first()
        
        yield{
            'Title':title,
            'URL': product_url,
            'Category 1': main_categories_name,
            'Category 2': sub_categories_name
        }



settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
