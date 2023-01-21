# -*- coding: utf-8 -*-

from lazy_crawler.puppeteer.puppeteer import browse
from lazy_crawler.lib.user_agent import get_user_agent

import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler

from bs4 import BeautifulSoup
from scrapy import Request, Spider
# import js2xml
# import dateparser
# import cloudscraper


class LazyCrawler(Spider):
    name = 'indeed'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 32,
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        data = browse('https://au.indeed.com/nurse-jobs-in-Australia', useragent=get_user_agent())
        
        yield data

    # count = 0

    # url = 'http://example.com/'

    # def start_requests(self):
    #     next_url = indeed[0]
    #     yield Request(self.url, self.parse, meta={'next_url': next_url}, dont_filter=True)

    # def parse(self, response):
    #     # url = response.meta['next_url']
    #     for i in range(1,66):
    #         self.count = self.count + 10
    #         url = 'https://au.indeed.com/jobs?q=nurse&l=Australia&start={}'.format(self.count)
    
    #         soup = self.get_soup(url)

    #         parse_job = self.parse_jobs(soup)

    #         for job in parse_job:
    #             yield Request(self.url, self.parse_again, meta={"job": job}, dont_filter=True)

    #     # next_url = get_next_page_url(soup)
    #     # if next_url:

    #     #     del url
    #     #     url = ''
    #     #     yield Request(self.url, callback=self.parse, meta={'next_url': next_url}, dont_filter=True)

    # def parse_again(self, response):
    #     res = response.meta['job']
    #     yield Request('http://example.com/', self.parse_job, meta={"job": res}, dont_filter=True)

    # def parse_job(self, response):
    #     job_dict = response.meta['job']
    #     job = {}
    #     jobkey = str(job_dict.get('jobkey'))
    #     job['jobkey'] = jobkey

    #     job['Job_Title'] = job_dict.get('title')

    #     job['Link'] = 'https://au.indeed.com/viewjob?jk=' + jobkey

    #     job['Address'] = job_dict.get('formattedLocation')
    #     job['state'] = job_dict.get('moreLinks', {}).get('locationName')
    #     frelative_time = job_dict.get('formattedRelativeTime')
    #     date_posted = dateparser.parse(frelative_time)
    #     if date_posted == None:
    #         if 'Just' in frelative_time:
    #             job['Date_Posted'] = str(
    #                 dateparser.parse('1 minutes ago').date())
    #         else:
    #             job['Date_Posted'] = str(
    #                 dateparser.parse('30 days ago').date())
    #     else:

    #         job['Date_Posted'] = str(date_posted.date())

    #     job['Urgent_Hire'] = job_dict.get('urgentlyHiring')

    #     job['Salary'] = job_dict.get('salarySnippet', {}).get('text')
    #     job['hot_job'] = 'no'
    #     job['Company'] = job_dict.get('company')

    #     job['Job_Type'] = ' | '.join(job_dict.get('jobTypes'))
    #     d_link = 'https://au.indeed.com/rc/clk?jk={jobkey}&atk='.format(
    #         jobkey=jobkey)
    #     job['Direct_Link'] = d_link

    #     yield job


    # def get_soup(self,url):
    #     print("*"*100, url)
    #     # scraper = cloudscraper.create_scraper(delay=10)
    #     scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
    #     response = scraper.get(url)
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     return soup


    # def parse_jobs(self, soup):
    #     script = soup.find('script', {'id': 'mosaic-data'}).text

    #     parsed = js2xml.parse(script)
    #     results = js2xml.jsonlike.make_dict(
    #         parsed.xpath('//property[@name="results"]/array')[0])

    #     return results

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
