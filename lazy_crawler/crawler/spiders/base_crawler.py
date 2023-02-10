import os
# import sys
import scrapy
# from scrapy.crawler import CrawlerProcess
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.loader import ItemLoader
# from scrapy.utils.project import get_project_settings
# from scrapy.loader import ItemLoader
# from lazy_crawler.lib.user_agent import get_user_agent

class LazyBaseCrawler(scrapy.Spider):

    # EXPORT_FILE = ''

    # if EXPORT_FILE == 'EXCEL':
    #     custom_settings = {
    #         'ITEM_PIPELINES' : {
    #             # 'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
    #             'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
    #             # "lazy_crawler.crawler.pipelines.MongoPipeline": 300,
    #             # 'reddit.pipelines.MongoPipeline': 300,
    #         }
    #     }

    # if EXPORT_FILE == "EXCEL":
    #     custom_settings = {}

    # def __init__(self, file_type ='EXCEL'):

    #     self.EXPORT_FILE = file_type

    #     if self.EXPORT_FILE == "EXCEL":
    #         custom_settings = {
    #             'ITEM_PIPELINES' : {
    #                 # 'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
    #                 'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
    #                 # "lazy_crawler.crawler.pipelines.MongoPipeline": 300,
    #                 # 'reddit.pipelines.MongoPipeline': 300,
    #             }
    #         }
    #     if self.EXPORT_FILE == 'JSON':
    #         custom_settings = {
    #             'ITEM_PIPELINES' : {
    #                 'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
    #                 # 'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
    #                 # "lazy_crawler.crawler.pipelines.MongoPipeline": 300,
    #                 # 'reddit.pipelines.MongoPipeline': 300,
    #             }
    #         }
        
    #     if self.EXPORT_FILE == 'CSV':
    #         custom_settings = {
    #             'ITEM_PIPELINES' : {
    #                 # 'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
    #                 'lazy_crawler.crawler.pipelines.CSVPipeline': 300
    #                 # "lazy_crawler.crawler.pipelines.MongoPipeline": 300,
    #                 # 'reddit.pipelines.MongoPipeline': 300,
    #             }
    #         }
    
    

        

    
    name = "lazy_base_crawler"

    allowed_domains = [""]

    # START URLS for your project.
    start_urls = ['']

# settings_file_path = 'lazy_crawler.crawler.settings'
# os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
# process = CrawlerProcess(get_project_settings())  
# process.crawl(LazyBaseCrawler)
# process.start() # the script will block here until the crawling is finished

