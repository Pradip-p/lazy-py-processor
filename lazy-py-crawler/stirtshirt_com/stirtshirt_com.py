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
from lazy_crawler.lib.image import process_image


class LazyCrawler(LazyBaseCrawler):

    name = "stirtshirt"

    def start_requests(self): #project start from here.
        
        settings = get_project_settings()
        # you can add the urls of category in python list.
        urls = ['https://stirtshirt.com/collections/halloween-shirt/','https://stirtshirt.com/collections/veterans-day/', 'https://stirtshirt.com/collections/valentines-day-gifts/','https://stirtshirt.com/collections/valentines-day-shirt/', 'https://stirtshirt.com/shop-the-holiday/','https://stirtshirt.com/collections/top-trending/','https://stirtshirt.com/collections/water-tracker-bottles/', 'https://stirtshirt.com/collections/campfire-mugs/','https://stirtshirt.com/collections/insulated-mugs-with-handle/','https://stirtshirt.com/collections/wine-tumblers/','https://stirtshirt.com/collections/stainless-steel-tumblers/','https://stirtshirt.com/collections/stainless-steel-bottles/' # 
                'https://stirtshirt.com/collections/funny-christmas-shirts/','https://stirtshirt.com/collections/disney-christmas-shirts/','https://stirtshirt.com/collections/most-likely-to-christmas-shirts/','https://stirtshirt.com/collections/couples-christmas-shirts/','https://stirtshirt.com/collections/friends-christmas-shirt/','https://stirtshirt.com/collections/family-christmas-shirts/','https://stirtshirt.com/collections/mens-christmas-shirts/','https://stirtshirt.com/collections/cute-christmas-shirts/',
                'https://stirtshirt.com/collections/christmas-pajama-shirts/', 'https://stirtshirt.com/collections/birthday-month-gift/',
                'https://stirtshirt.com/collections/january-birthday-gift/',' https://stirtshirt.com/collections/february-birthday-gift/',' https://stirtshirt.com/collections/march-birthday-gift/','https://stirtshirt.com/collections/april-birthday-gift/','https://stirtshirt.com/collections/may-birthday-gift/',' https://stirtshirt.com/collections/june-birthday-gift/',
                'https://stirtshirt.com/collections/july-birthday-gift/','https://stirtshirt.com/collections/august -birthday-gift/','https://stirtshirt.com/collections/september -birthday-gift/',' https://stirtshirt.com/collections/october -birthday-gift/','https://stirtshirt.com/collections/november-birthday-gift/','https://stirtshirt.com/collections/december-birthday-gift/','https://stirtshirt.com/collections/milestone-birthday-gift/','https://stirtshirt.com/collections/7th-birthday-gift/',
                'https://stirtshirt.com/collections/10th-birthday-gift/', 
                'https://stirtshirt.com/collections/10th-birthday-gift/', 'https://stirtshirt.com/collections/16th-birthday-gift/','https://stirtshirt.com/collections/18th-birthday-gift/', 'https://stirtshirt.com/collections/20th-birthday-gift/', 'https://stirtshirt.com/collections/21th-birthday-gift/', 'https://stirtshirt.com/collections/30th-birthday-gift/', 'https://stirtshirt.com/collections/40th-birthday-gift/', 'https://stirtshirt.com/collections/50th-birthday-gift/',' https://stirtshirt.com/collections/60th-birthday-gift/']


        # urls = ['https://stirtshirt.com/collections/halloween-shirt/']

        for url in urls:        
            yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        # urls => extract all url of product from one page
        urls = response.xpath('//div[@class="product-small box "]/div[@class="box-image"]/div[@class="image-zoom_in"]/a/@href').extract()

        # to get next page url if available 
        next_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        
        for url in urls:
            
            # send the requst for each product details
            yield scrapy.Request(url, self.parse_detail, dont_filter=True)
        
        # to send next page until next page available.
        if next_url:
            yield scrapy.Request(next_url, self.parse, dont_filter=True)


    def parse_detail(self, response):
        title = response.xpath('//meta[@property="og:image:alt"]/@content').extract_first()
        image_url = response.xpath('//meta[@property="og:image:secure_url"]/@content').extract_first()
        price = response.xpath('//meta[@name="twitter:data1"]/@content').extract_first()
        desc = response.xpath('//div[@id="tab-description"]//text()').extract()
        desc = [re.sub(r'[\r\n\t]', '', x) for x in desc]
        image_name = image_url.split('?')[0].split('/')[-1]
        
        img = process_image(image_url,image_name)

        # print(img)
        # ipdb.set_trace()
        
        #send to wordpress api https://shirtof.com/

        url = 'https://shirtof.com/wp-json/wp/v2/posts'

        user = 'demo'

        password = '3tEv efYM w30d 7Asn 9hS9 QilX'

        credentials = user + ':' + password


        # token = base64.b64decode(creds.encode())
        token = base64.b64encode(credentials.encode())
        

        header = {'Authorization': 'Basic ' + token.decode('utf-8'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        }

        fileName = os.path.basename('image.png')

        data = open(img, 'rb')

        media = {
            'file':data, #data
            'caption': title,
            'description': title,
        }
        # print("#"*100)
        image_url = 'https://shirtof.com/wp-json/wp/v2/media'

        header1 ={ 'Authorization': 'Basic ' + token.decode('utf-8'),
            'cache-control': 'no-cache',
            'mime_type':"image/png",
            # 'content-type': 'image/png','content-disposition' : 'attachment; filename="image.png"',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        }

        image = requests.post(image_url, headers=header1, files=media)
    
        # ['source_url']
        imageURL = json.loads(image.content)
        imageURL = imageURL.get('source_url')

        post ={
            'date': '2022-03-23T10:00:00',
            'title':title,
            # 'content': desc,
            'content':  '<img src="'+ imageURL + ' ">'+ str(desc),
            # 'content': 'This is test wordpress api',
            "status":'publish'
        }
        r = requests.post(url , headers=header, json=post)


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
