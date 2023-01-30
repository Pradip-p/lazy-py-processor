# https://www.indeed.com/?from=gnav-homepage
import os
from lazy_crawler.puppeteer.puppeteer import browse
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import dateparser
import cloudscraper
from bs4 import BeautifulSoup
import js2xml
from lxml import html
import scrapy

class LazyCrawler(LazyBaseCrawler):

    name = "indeed"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 5, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,

        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
        }
    }

    

    def start_requests(self):
        url = 'https://www.indeed.com/?from=gnav-homepage'
        soup = self.get_soup(url)

        parse_job = self.parse_jobs(soup)
        print(parse_job)
        yield scrapy.Request('http://example.com/', self.parse, dont_filter=True)

    def parse(self, response):
        yield {}
    #     # url = response.meta['next_url']
    #     for i in range(1,66):
    #         self.count = self.count + 10
    #         url = 'https://au.indeed.com/jobs?q=nurse&l=Australia&start={}'.format(self.count)
    
    #         soup = self.get_soup(url)

    #         parse_job = self.parse_jobs(soup)

    #         for job in parse_job:
    #             yield scrapy.Request(self.url, self.parse_again, meta={"job": job}, dont_filter=True)


    # def parse_again(self, response):
    #     res = response.meta['job']
    #     yield scrapy.Request('http://example.com/', self.parse_job, meta={"job": res}, dont_filter=True)

    def parse_job(self, response):
        job_dict = response.meta['job']
        job = {}
        jobkey = str(job_dict.get('jobkey'))
        job['jobkey'] = jobkey

        job['Job_Title'] = job_dict.get('title')

        job['Link'] = 'https://au.indeed.com/viewjob?jk=' + jobkey

        job['Address'] = job_dict.get('formattedLocation')
        job['state'] = job_dict.get('moreLinks', {}).get('locationName')
        frelative_time = job_dict.get('formattedRelativeTime')
        date_posted = dateparser.parse(frelative_time)
        if date_posted == None:
            if 'Just' in frelative_time:
                job['Date_Posted'] = str(
                    dateparser.parse('1 minutes ago').date())
            else:
                job['Date_Posted'] = str(
                    dateparser.parse('30 days ago').date())
        else:

            job['Date_Posted'] = str(date_posted.date())

        job['Urgent_Hire'] = job_dict.get('urgentlyHiring')

        job['Salary'] = job_dict.get('salarySnippet', {}).get('text')
        job['hot_job'] = 'no'
        job['Company'] = job_dict.get('company')

        job['Job_Type'] = ' | '.join(job_dict.get('jobTypes'))
        d_link = 'https://au.indeed.com/rc/clk?jk={jobkey}&atk='.format(
            jobkey=jobkey)
        job['Direct_Link'] = d_link

        yield job


    def get_soup(self,url):
        print("*"*100, url)
        data = browse(url, useragent=get_user_agent('random'))
        content = data['content']
        tree = html.fromstring(content)
        with open('test.txt', 'w') as f:
            f.write(str(content))
        # scraper = cloudscraper.create_scraper(delay=100)
        # # scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
        # response = scraper.get(url)
        # soup = BeautifulSoup(response.text, 'lxml')
        # return soup


    def parse_jobs(self, soup):
        script = soup.find('script', {'id': 'mosaic-data'}).text
        with open('save.txt', 'w') as f:
            f.write(str(script))
        # print(script)
        # parsed = js2xml.parse(script)
        # # print(parsed)
        # print(js2xml.pretty_print(parsed))
        # print(parsed.xpath('//property[@name="results"]'))
        # results = js2xml.jsonlike.make_dict(parsed.xpath('//property[@name="results"]'))
        # print(results)
        # return results

    #     yield {
    #     'id': '',
    #     'company_name': 'Shopify',
    #     'job_title': JobTitle,
    #     'country': country,
    #     'city': '',
    #     'job_application_url':job_application_url,
    #     'job_description': roleDescription,
    #     'job_type': '',
    #     'min_salary': '',
    #     'max_salary': '',
    #     'fixed_salay': '',
    #     'salary_currency': '',
    #     'division':division,
    #     'company_logo': '',
    #     'salary_interval': '',
    #     'remote_work_policy': '',
    #     'company_bio': ''.join(company_bio),
    #     }

        



settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished

