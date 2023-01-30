#PID: 5 Description: thread_test

import base64
import json
import os
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import re
# from lazy_crawler.lib.image import process_image
# from lazy_crawler.lib.html import to_browser


class LazyCrawler(LazyBaseCrawler):

    name = "arbeitnow"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls', 'RETRY_TIMES': 200, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180
    }

    def start_requests(self):
        data = {"n":"pageview","u":"https://www.arbeitnow.com/","d":"arbeitnow.com","r":'null',"w":'1920'}

        url = 'https://stats.arbeitnow.com/api/event'
        print('calling....................')
        try:
            yield scrapy.FormRequest(url, formdata=data, callback=self.parse_items, dont_filter=True)
        except ValueError as e:
            print(e)

    # start_urls = ['https://www.arbeitnow.com/?search=&tags=&sort_by=relevance&page=1']

    def parse_items(self, response):
        print(response.status)
        # urls = response.xpath('//a/@href').extract()
        # print(urls)

        # urls = response.xpath('//div[@class="py-2"]').extract()
        # print(urls)
        # # urls => extract all url of product from one page
        # urls = response.xpath('//div[@class="product-small box "]/div[@class="box-image"]/div[@class="image-zoom_in"]/a/@href').extract()

        # # to get next page url if available 
        # next_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        
        # for url in urls:
            
        #     # send the requst for each product details
        #     yield scrapy.Request(url, self.parse_detail, dont_filter=True)
        
        # to send next page until next page available.
        # if next_url:
        #     yield scrapy.Request(next_url, self.parse, dont_filter=True)


    # def parse_detail(self, response):
    #     title = response.xpath('//meta[@property="og:image:alt"]/@content').extract_first()
    #     image_url = response.xpath('//meta[@property="og:image:secure_url"]/@content').extract_first()
    #     price = response.xpath('//meta[@name="twitter:data1"]/@content').extract_first()
    #     desc = response.xpath('//div[@id="tab-description"]//text()').extract()
    #     desc = [re.sub(r'[\r\n\t]', '', x) for x in desc]
    #     image_name = image_url.split('?')[0].split('/')[-1]
        
    #     img = process_image(image_url,image_name)

    #     # print(img)
    #     # ipdb.set_trace()
        
    #     #send to wordpress api https://shirtof.com/

    #     url = 'https://shirtof.com/wp-json/wp/v2/posts'

    #     user = 'demo'

    #     password = '3tEv efYM w30d 7Asn 9hS9 QilX'

    #     credentials = user + ':' + password


    #     # token = base64.b64decode(creds.encode())
    #     token = base64.b64encode(credentials.encode())
        

    #     header = {'Authorization': 'Basic ' + token.decode('utf-8'),
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    #     }

    #     fileName = os.path.basename('image.png')

    #     data = open(img, 'rb')

    #     media = {
    #         'file':data, #data
    #         'caption': title,
    #         'description': title,
    #     }
    #     # print("#"*100)
    #     image_url = 'https://shirtof.com/wp-json/wp/v2/media'

    #     header1 ={ 'Authorization': 'Basic ' + token.decode('utf-8'),
    #         'cache-control': 'no-cache',
    #         'mime_type':"image/png",
    #         # 'content-type': 'image/png','content-disposition' : 'attachment; filename="image.png"',
    #         'Accept': 'application/json',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    #     }

    #     image = requests.post(image_url, headers=header1, files=media)
    
    #     # ['source_url']
    #     imageURL = json.loads(image.content)
    #     imageURL = imageURL.get('source_url')

    #     post ={
    #         'date': '2022-03-23T10:00:00',
    #         'title':title,
    #         # 'content': desc,
    #         'content':  '<img src="'+ imageURL + ' ">'+ str(desc),
    #         # 'content': 'This is test wordpress api',
    #         "status":'publish'
    #     }
    #     r = requests.post(url , headers=header, json=post)


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
