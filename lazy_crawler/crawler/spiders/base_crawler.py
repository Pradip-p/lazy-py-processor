import os
import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
# from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from lazy_crawler.lib.user_agent import get_user_agent

class LazyBaseCrawler(scrapy.Spider):
    
    name = "lazy_base_crawler"

    allowed_domains = [""]

    # START URLS for your project.
    start_urls = ['']
    
    # custom_settings = {
    #     # 'ITEM_PIPELINES': {  
    #     #     "lazy_crawler.crawler.pipelines.MongoPipeline": 300
    #     # },
        
    #     "name": "lazy_base_crawler",
    #     "ITEM_PIPELINES" : {
    #         'lazy_crawler.crawler.pipelines.AmazonPipeline': 300
    #     }
    # }
    
    

