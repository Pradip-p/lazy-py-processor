import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
import base64
from lazy_crawler.lib.user_agent import get_user_agent
import gc

class LazyCrawler(LazyBaseCrawler):

    name = "englishelm"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 32,'CONCURRENT_REQUESTS_PER_IP': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,'RETRY_TIMES': 200,
        "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,
        'ITEM_PIPELINES' :  {
        'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
        }
    }
    categories = [
        {'living':['https://englishelm.com/collections/sofas','https://englishelm.com/collections/sectionals',
        'https://englishelm.com/collections/loveseats','https://englishelm.com/collections/chaise','https://englishelm.com/collections/living-room-sets',
        'https://englishelm.com/collections/accent-armchairs','https://englishelm.com/collections/accent-chairs','https://englishelm.com/collections/benches',
        'https://englishelm.com/collections/daybeds','https://englishelm.com/collections/poufs','https://englishelm.com/collections/end-tables',
        'https://englishelm.com/collections/console-tables','https://englishelm.com/collections/coffee-tables','https://englishelm.com/collections/ottomans-and-trunks',
        'https://englishelm.com/collections/nesting-tables','https://englishelm.com/collections/bookcases-and-shelves','https://englishelm.com/collections/entertainment-centers',
        'https://englishelm.com/collections/coat-racks-and-hangers','https://englishelm.com/collections/display-cabinets','https://englishelm.com/collections/wine-cabinets'
        ]
        },
        {
            'dining':[
                'https://englishelm.com/collections/dining-chairs','https://englishelm.com/collections/dining-tables','https://englishelm.com/collections/dining-sets','https://englishelm.com/collections/dining-sets',
                'https://englishelm.com/collections/barstools-and-counterstools','https://englishelm.com/collections/stools','https://englishelm.com/collections/bar-tables','https://englishelm.com/collections/kitchen-island-tables',
                'https://englishelm.com/collections/buffets-and-sideboards','https://englishelm.com/collections/kitchen-accessories'
            ]
        },
        {
            'bed':[
                'https://englishelm.com/collections/twin-beds','https://englishelm.com/collections/full-beds','https://englishelm.com/collections/queen-beds',
                'https://englishelm.com/collections/king-beds','https://englishelm.com/collections/california-king-beds','https://englishelm.com/collections/bed-frames',
                'https://englishelm.com/collections/bedroom-sets','https://englishelm.com/collections/comforters','https://englishelm.com/collections/sheets',
                'https://englishelm.com/collections/duvets','https://englishelm.com/collections/throws','https://englishelm.com/collections/vanities','https://englishelm.com/collections/armoires',
                'https://englishelm.com/collections/nightstands','https://englishelm.com/collections/dressers-and-chests','https://englishelm.com/collections/pillows',
                'https://englishelm.com/collections/mattresses','https://englishelm.com/collections/headboards','https://englishelm.com/collections/mirrors',
                'https://englishelm.com/collections/curtains','https://englishelm.com/collections/window-panels'
            ]
        },
        {
            'lighting':[
                'https://englishelm.com/collections/ceiling-lights','https://englishelm.com/collections/wall-lights',
                'https://englishelm.com/collections/floor-lamps','https://englishelm.com/collections/table-lamps'
            ]
        },
        {
            'rugs':[
                'https://englishelm.com/collections/rugs/Black','https://englishelm.com/collections/rugs/Blue','https://englishelm.com/collections/rugs/Brown',
                'https://englishelm.com/collections/rugs/Green','https://englishelm.com/collections/rugs/Pink','https://englishelm.com/collections/rugs/Red',
                'https://englishelm.com/collections/rugs/Yellow','https://englishelm.com/collections/rugs/White','https://englishelm.com/collections/rugs/Wool',
                'https://englishelm.com/collections/rugs/Jute','https://englishelm.com/collections/rugs/Olefin','https://englishelm.com/collections/rugs/Polyester',
                'https://englishelm.com/collections/rugs/Leather','https://englishelm.com/collections/rugs/Square','https://englishelm.com/collections/rugs/Round',
                'https://englishelm.com/collections/rugs/Oval','https://englishelm.com/collections/rugs/Octagon','https://englishelm.com/collections/rugs/Runner',
                'https://englishelm.com/collections/rugs/Rectangle'
            ]
        },
        {
            'outdoor':[
                'https://englishelm.com/collections/outdoor-sets','https://englishelm.com/collections/outdoor-accent-chairs-and-benches','https://englishelm.com/collections/outdoor-daybeds',
                'https://englishelm.com/collections/outdoor-dining-chairs','https://englishelm.com/collections/outdoor-dining-tables','https://englishelm.com/collections/outdoor-lounge-and-chaise',
                'https://englishelm.com/collections/outdoor-occasional-tables','https://englishelm.com/collections/outdoor-sectionals','https://englishelm.com/collections/outdoor-sofas',
                'https://englishelm.com/collections/outdoor-umbrellas','https://englishelm.com/collections/outdoor-accessories'
            ]
        },
        {
            'accessories':[
                'https://englishelm.com/collections/containers','https://englishelm.com/collections/baskets','https://englishelm.com/collections/planters',
                'https://englishelm.com/collections/wall-art','https://englishelm.com/collections/decorative-art-pieces','https://englishelm.com/collections/statues',
                'https://englishelm.com/collections/bookends','https://englishelm.com/collections/picture-frames','https://englishelm.com/collections/vases',
                'https://englishelm.com/collections/clocks','https://englishelm.com/collections/amenity-boxes','https://englishelm.com/collections/candle-holders','https://englishelm.com/collections/magazine-holders',
                'https://englishelm.com/collections/room-dividers-and-screens'
            ]
        },
        {
            'kitchen':[
                'https://englishelm.com/collections/dinnerware-sets','https://englishelm.com/collections/plates','https://englishelm.com/collections/bowls','https://englishelm.com/collections/glasses',
                'https://englishelm.com/collections/mugs','https://englishelm.com/collections/wine','https://englishelm.com/collections/plates-and-trays',
                'https://englishelm.com/collections/serving-bowls','https://englishelm.com/collections/sugar-bowls','https://englishelm.com/collections/pitchers',
                'https://englishelm.com/collections/flatware-sets','https://englishelm.com/collections/bakers-casseroles','https://englishelm.com/collections/dutch-ovens',
                'https://englishelm.com/collections/frypans','https://englishelm.com/collections/grill-pans','https://englishelm.com/collections/saucepans','https://englishelm.com/collections/skillets',
                'https://englishelm.com/collections/stewpans','https://englishelm.com/collections/woks',
                'https://englishelm.com/collections/pie-dishes','https://englishelm.com/collections/ramekins','https://englishelm.com/collections/knives',
                'https://englishelm.com/collections/cutting-boards','https://englishelm.com/collections/measuring-scales','https://englishelm.com/collections/tongs-whisks',
                'https://englishelm.com/collections/spatulas-turners','https://englishelm.com/collections/ladles-spoons'
            ]
        }
    ]

    proxy = 'p.webshare.io:80'
    user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    
    def start_requests(self): #project start from here.
        for category in self.categories:
            category = category.items()
            for key, value in category:
                category_name = key
                urls = value
                for url in urls:
                    yield scrapy.Request(url, self.parse, dont_filter=True,
                        meta={'proxy': 'http://' + self.proxy, 'category_name':category_name},
                        headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
                        'User-Agent': get_user_agent('random')
                        })

    def parse(self, response):
        category_name = response.meta['category_name']
        urls = response.xpath('//div[@class="product-image image-swap"]/a[@class="product-grid-image"]/@href').extract()
        for _url in urls:
            url = 'https://englishelm.com{}{}'.format(_url,'.js')
            product_url = 'https://englishelm.com{}'.format(_url)
            yield scrapy.Request(url, self.parse_details, dont_filter=True, 
            meta={'proxy': 'http://' + self.proxy,
            'product_url':product_url,
            'category_name':category_name
            },
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            })

        next_page = response.xpath('//ul[@class="pagination-page"]/li[@class="text"]/a[@title="Next"]/@href').extract_first()
        if next_page:
            url = 'https://englishelm.com{}'.format(next_page)
            yield scrapy.Request(url, self.parse, dont_filter=True,
            meta={'proxy': 'http://' + self.proxy,
            'category_name':category_name
            },
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            })
    def parse_details(self, response):
        res = response.json()
        # title = res['title']
        description = res['description']
        vendor = res['vendor']
        _type = res['type']
        # tags = res['tags']
        # price = res['price']
        # price_min = res['price_min']
        # price_max = res['price_max']
        # available = res['available']
        # price_varies = res['price_varies']
        
        # image_urls = []
        # for url in images:
        #     url = 'https:{}'.format(url)
        #     image_urls.append(url)
        # if image_urls:
        #     image_urls = '|'.join(image_urls)
        
        # else:
        #     image_urls = ''
        # featured_image = 'https:{}'.format(res['featured_image'])

        images = res['images']
        variants = res['variants']
        for variant in variants:
            created_at = ''
            updated_at = ''
            if variant['featured_image']:
                created_at = variant['featured_image'].get('created_at')
                updated_at = variant['featured_image'].get('updated_at')
                
            sku = variant['sku'].strip()
            image_url = []
            for image in images:
                if sku in image:
                    image = 'https:{}'.format(image)
                    image_url.append(image)
                else:
                    if sku.lower() in image:
                        image = 'https:{}'.format(image)
                        image_url.append(image)
            available = variant['available']
            if available:
                available = 'Yes'
            else:
                available = 'No'
            price = int(variant['price'])/100
            inventory_management = variant['inventory_management']
            name = variant['name']
            barcode = variant['barcode']

            yield{
                'upc': barcode,
                'sku':sku,
                'category': response.meta['category_name'],
                'vendor':vendor,
                'product_name': name,
                'price': price,
                'product_url': response.meta['product_url'],
                'image_url': ' | '.join(image_url),
                'description': strip_html(str(description)),
                'available': available,
                'type':_type,
                'inventory_management': inventory_management,
                'created_at':created_at,
                'updated_at':updated_at
            }
            
            gc.collect()


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished