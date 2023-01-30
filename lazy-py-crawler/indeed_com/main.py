from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.puppeteer.puppeteer import browse
from lazy_crawler.lib.user_agent import get_user_agent
from lxml import html
import scrapy
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler

class AmazonScrapper(LazyBaseCrawler):
    start_urls = ['https://www.amazon.com/s?k=chocolate']

    def __init__(self):
        self.asin_list = self.get_asin('https://www.amazon.com/s?k=chocolate')
        print(self.asin_list)
        for asin in self.asin_list:
            url = 'https://www.amazon.com/dp/{}'.format(asin)
            print(self.get_product_details(url))

    def get_asin(self,url):
        data = browse(url, useragent=get_user_agent('random'))
        content = data['content']
        tree = html.fromstring(content)
        asin = tree.xpath('//div[@data-component-type="s-search-result"]/@data-asin')
        return asin


    def get_product_details(self, url):
        product_detail = {}
        data = browse(url, useragent=get_user_agent('random'))
        content = data['content']
        tree = html.fromstring(content)
        title = tree.xpath('//span[@id="productTitle"]/text()')
        rating = tree.xpath('//span[@id="acrCustomerReviewText"]/text()')
        product_desc = ''.join(tree.xpath('//div[@id="productDescription"]//text()'))
        #product details
        product_details = tree.xpath('//div[@id="detailBullets_feature_div"]/ul')
        # print(product_details)
        product_detail['Title'] = title
        product_detail['Rating'] = rating
        product_detail['product_desc'] = product_desc
        for product in product_details:
            key = ''.join(product.xpath('//li/span[@class="a-list-item"]/span[@class="a-text-bold"]/text()')).strip()
            value = ''.join(product.xpath('//li/span[@class="a-list-item"]/span/text()')).strip()
            product_detail[key] = value

        yield product_detail

def linkedinScraper(event, context):
    def script(queue):
        try:
            settings = get_project_settings()

            settings.setdict({
                'LOG_LEVEL': 'ERROR',
                'LOG_ENABLED': True,
            })

            process = CrawlerProcess(settings)
            process.crawl(AmazonScrapper)
            process.start()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    queue = Queue()

    # wrap the spider in a child process
    main_process = Process(target=script, args=(queue,))
    main_process.start()    # start the process
    main_process.join()     # block until the spider finishes

    result = queue.get()    # check the process did not return an error
    if result is not None:
        raise result


# if __name__ == "__linkedinScraper__":
    # linkedinScraper("event","context")
linkedinScraper("event","context")