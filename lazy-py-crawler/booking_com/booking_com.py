
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.mylogger import Logger
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.exceptions import NotConfigured
import logging
from urllib.parse import urlencode
from lazy_crawler.lib.html import to_browser

# from lazy_crawler.puppeteer.puppeteer import browse

class LazyCrawler(LazyBaseCrawler):

    logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
    )
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 126,'CONCURRENT_REQUESTS_PER_IP': 26,'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
    }

    name = "booking"

    settings = get_project_settings()

    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
}
    """scrapes a single hotel search page of booking.com"""

    checkin: str = ""
    checkout: str = ""
    number_of_rooms=1
    offset: int = 0

    checkin_year, checking_month, checking_day = checkin.split("-") if checkin else "", "", ""
    checkout_year, checkout_month, checkout_day = checkout.split("-") if checkout else "", "", ""

    url = "https://www.booking.com/searchresults.de.html"

    query = 'Siem Reap'
    
    def start_requests(self): #project start from here.

        self.url += "?" + urlencode(
        {
            "ss": self.query,
            "checkin_year": self.checkin_year,
            "checkin_month": self.checking_month,
            "checkin_monthday": self.checking_day,
            "checkout_year": self.checkout_year,
            "checkout_month": self.checkout_month,
            "checkout_monthday": self.checkout_day,
            "no_rooms": self.number_of_rooms,
            "offset": self.offset,
        }
    )

        yield scrapy.Request(self.url, self.parse_data, dont_filter=True,  headers=self.HEADERS)
    

    def parse_data(self, response):
        to_browser(response)

        # sel = scrapy.Selector(response)
        print(response.xpath('//div[@data-testid="title"]/text()').extract())

        hotel_previews = {}
        # for hotel_box in sel.xpath('//div[@data-testid="property-card"]'):
        #     url = hotel_box.xpath('.//h3/a[@data-testid="title-link"]/@href').get("").split("?")[0]
        #     hotel_previews[url] = {
        #         "name": hotel_box.xpath('.//h3/a[@data-testid="title-link"]/div/text()').get(""),
        #         "location": hotel_box.xpath('.//span[@data-testid="address"]/text()').get(""),
        #         "score": hotel_box.xpath('.//div[@data-testid="review-score"]/div/text()').get(""),
        #         "review_count": hotel_box.xpath('.//div[@data-testid="review-score"]/div[2]/div[2]/text()').get(""),
        #         "stars": len(hotel_box.xpath('.//div[@data-testid="rating-stars"]/span').getall()),
        #         "image": hotel_box.xpath('.//img[@data-testid="image"]/@src').get(),
        #     }
        yield hotel_previews


    


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
