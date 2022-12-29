
# LazyPyProcessor

Customized Scrapy is a modified version of the popular open-source web scraping framework, Scrapy, that is designed for easy of setup and use. It includes a predefined library of functions and utilities that make it easy to extract and process data from websites.

##### Note. This library was written for python3 and scrapy1.6.0. However higher version is supported.

### Installation Instruction
    Create a virtual environment for your project. Install Customized Scrapy using `pip`:
```
pip install git+https://github.com/Pradip-p/lazy-py-processor.git

```
or
Alternatively, you can install LazyPyProcessor Scrapy by cloning the repository and installing it locally:
```pip install . ```


###### Note if you are having installation issue. please check if you have added your public ssh keys to github. Visit this blog for more details on adding ssh keys to github
[https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

### Visit documentation here

#### It is recommended to take a look at scrapy documentation also as this library merly hides setup complexity of scrapy and some other settings. You would still need to learn scrapy framework for using spiders.

https://docs.scrapy.org/en/latest/


## Build instructions

We use semantic versioning(https://en.wikipedia.org/wiki/Software_versioning)

In order to build the docker container.

1. Commit your changes.
2. Increase the version(patch, minor , major)

    Normally, its patch
    
    Install bumpversion for easier version management.
    
    In order to increase patch version simply do
    `bumpversion patch`
    
    For example if the current tag is 1.04
    Doing `bumpversion patch` will make the tag 1.05
    
3. push to tags
```git push --tags```

4. Also push to master branch
``` git push origin master```

### Usage
### To use LazyPyProcessor 
##### make a python file for your project (example: `scrapy_example.py`)


```
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.mylogger import Logger
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.exceptions import NotConfigured
import logging

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

    name = "laptop"

    settings = get_project_settings()

    settings.set('LOG_FILE','Log.log',priority='cmdline')
    
    
        
    headers = get_user_agent('random')

    def start_requests(self): #project start from here.
        
        # for url in urls:
        url = 'https://latop10.it/auto/'
        yield scrapy.Request(url, self.parse_get_sub_categories, dont_filter=True, )



    def parse_get_sub_categories(self, response):
        # browse(response.url, False)
        Logger()

        sub_categories_urls = response.xpath('//main[@id="genesis-content"]/article/header[@class="entry-header"]/h2[@class="entry-title"]/a[@class="entry-title-link"]/@href').extract()
    
        next_page_url = response.xpath('//div[@class="archive-pagination pagination"]/ul/li[@class="pagination-next"]/a/@href').extract_first()
        
        for url in sub_categories_urls:
        
            yield scrapy.Request(url, self.get_product_details, dont_filter=True,)

        if next_page_url:
            yield scrapy.Request(next_page_url, self.parse_get_sub_categories, dont_filter=True)

    def get_product_details(self, response):
        main_categories_name = response.xpath('//div[@class="content-sidebar-wrap"]/p[@id="breadcrumbs"]/span/span/span/a/text()').extract_first()
        sub_categories_name = response.xpath('//div[@class="content-sidebar-wrap"]/p[@id="breadcrumbs"]/span/span/span/span/a/text()').extract_first()
        
        product_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        try:
            title = response.xpath('//main[@id="genesis-content"]/article/header[@class="entry-header"]/h1[@class="entry-title"]/text()').extract_first()
        except Exception:
            NotConfigured("")
        yield{
            'Title':title,
            'URL': product_url,
            'Category 1': main_categories_name,
            'Category 2': sub_categories_name
        }

    


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
```
## Further resources

For more information and examples of how to use Lazy Py Processor, see the project documentation.
## Credits

Lazy Py Processor was created by Pradip p.

## License

Lazy Py Processor is released under the MIT License.