import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import ipdb


class LazyCrawler(LazyBaseCrawler):

    name = "freida"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 120,'CONCURRENT_REQUESTS_PER_IP': 26,'CONCURRENT_REQUESTS_PER_DOMAIN': 26,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,
        'ITEM_PIPELINES' : {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
            }
        }
    
    start_urls = ['https://freida-admin.ama-assn.org/api/node/program?page[offset]=0&page[limit]=50']
    # count = 0

    # def start_requests(self):
    #     for i in range(24):
    #         url = 'https://freida-admin.ama-assn.org/api/node/program?page[offset]='+str(self.count)+'&page[limit]=50'
    #         self.count += 50
    #         yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        res = response.json()
        for data in res['data']:
            id_= data['id']
            url = 'https://freida-admin.ama-assn.org/api/node/program/'+id_+'?include=field_specialty,field_survey.field_program_director,field_survey.field_program_contact,field_survey.field_primary_teaching_site,field_institution,field_participant_institution'
            yield scrapy.Request(url, self.parse_get_program_details, dont_filter=True)
        
        next_url = res['links']['next'].get('href')
        # self_url = res['links']['self'].get('href')

        if next_url:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_get_program_details(self, response):
        res = response.json()
        data = res['data']
        title = data['attributes'].get('title')

        #for Program coordinator
        included = res['included']
        for inc in included:
            #Program Director
            if inc['attributes'].get('parent_field_name') == 'field_program_director':
            
                field_first_name =  inc['attributes'].get('field_first_name') 
                field_degrees = inc['attributes'].get('field_degrees')
                field_last_name = inc['attributes'].get('field_last_name')
                field_middle_name = inc['attributes'].get('field_middle_name')
                dr_field_email = inc['attributes'].get('field_email')

                if field_middle_name == None:
                    field_middle_name = ''
                if field_first_name == None:
                    field_first_name = ''
                if field_last_name == None:
                    field_last_name = ''
                if field_degrees == None:
                    field_degrees = ''
                program_director = field_first_name + field_middle_name + field_last_name + field_degrees
                
            # field_program_contact / Other
            if inc['attributes'].get('parent_field_name') == 'field_program_contact':
                field_first_name = inc['attributes'].get('field_first_name')
                field_degrees = inc['attributes'].get('field_degrees')
                field_last_name = inc['attributes'].get('field_last_name')
                field_middle_name = inc['attributes'].get('field_middle_name')
                co_field_email = inc['attributes'].get('field_email')
                if field_middle_name == None:
                    field_middle_name = ''
                if field_first_name == None:
                    field_first_name = ''
                if field_last_name == None:
                    field_last_name = ''
                if field_degrees == None:
                    field_degrees = ''

                co_program_director = field_first_name + field_middle_name + field_last_name + field_degrees
            program = inc['attributes'].get('title')

        yield{
            'Title':title,
            'Program':program,
            'Program Director':program_director,
            'Program Director Email':dr_field_email,
            'Other/Coordinator':co_program_director,
            'Other/Coordinator Email': co_field_email
        }



settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
