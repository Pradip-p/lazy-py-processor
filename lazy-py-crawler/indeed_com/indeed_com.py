# -*- coding: utf-8 -*-

from lazy_crawler.puppeteer.puppeteer import browse
from lazy_crawler.lib.user_agent import get_user_agent

# import os
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
# import asyncio
# from bs4 import BeautifulSoup
# from scrapy import Request, Spider

from lxml import html

def get_asin(url):
    data = browse(url, useragent=get_user_agent('random'))
    content = data['content']
    tree = html.fromstring(content)
    asin = tree.xpath('//div[@data-component-type="s-search-result"]/@data-asin')
    return asin


def get_product_details(url):
    product_detail = {}
    data = browse(url, useragent=get_user_agent('random'))
    content = data['content']
    tree = html.fromstring(content)
    title = tree.xpath('//span[@id="productTitle"]/text()')
    rating = tree.xpath('//span[@id="acrCustomerReviewText"]/text()')
    product_desc = tree.xpath('//div[@id="productDescription"]//text()')
    #product details
    product_details = tree.xpath('//div[@id="detailBullets_feature_div"]/ul')
    # print(product_details)
    product_detail['Title'] = title
    product_detail['Rating'] = rating

    for product in product_details:
        key = ''.join(product.xpath('//li/span[@class="a-list-item"]/span[@class="a-text-bold"]/text()')).strip()
        value = ''.join(product.xpath('//li/span[@class="a-list-item"]/span/text()')).strip()
        product_detail[key] = value

    return product_detail


if __name__=='__main__':
    data = browse('https://www.rent.com/', useragent=get_user_agent('random'))
    print(data)
    # asin_list = get_asin('https://www.amazon.com/s?k=chocolate')
    # for asin in asin_list:
    #     url = 'https://www.amazon.com/dp/{}'.format(asin)
    #     get_product_details(url)


