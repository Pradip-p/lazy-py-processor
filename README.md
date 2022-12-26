
# scrapy python library 

##### Note. This library was written for python3 and scrapy1.6.0. However higher version is supported.

### Installation Instruction
* Create a virtual env
* Install it as you would install python package
```
pip install git+ssh://github.com/Pradip-p/lazy-py-processor.git
```
or
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

### Example for scraping data from a website
##### make a python file for your project (example: `scrapy_example.py`)

```
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ScrapyCrawler(scrapy.Spider):
        
    name = "quotes"
    
    def start_requests(self):
        settings = get_project_settings()
        
        print("Your USER_AGENT is:\n%s" % (settings.get('ITEM_PIPELINES')))
        
        url = 'http://quotes.toscrape.com/'
        
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('small.author::text').get(),
                'text': quote.css('span.text::text').get(),
                'tag':quote.css('.tags a.tag::text').get(),
                
                
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        
settings_file_path = 'scrapy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(ScrapyCrawler)
process.start() # the script will block here until the crawling is finished 
```
