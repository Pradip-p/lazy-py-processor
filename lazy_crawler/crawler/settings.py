# -*- coding: utf-8 -*-
import os
from lazy_crawler.lib.user_agent import get_user_agent
from lazy_crawler.lib.proxy import get_proxy
# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "lazy_py_crawler"

SPIDER_MODULES = ["lazy_crawler.crawler.spiders"]
NEWSPIDER_MODULE = "lazy_crawler.crawler.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent

# if os.environ.get('APP_ENV', 'DEV').lower() == 'prd':
#     LOG_LEVEL = 'ERROR'
# else:
#     LOG_LEVEL = 'DEBUG'
# Obey robots.txt rules

ROBOTSTXT_OBEY = False


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 256

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 256
CONCURRENT_REQUESTS_PER_IP = 256

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.VtxScrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.VtxScrapyDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
    'lazy_crawler.crawler.pipelines.CSVPipeline': 300
    }

RETRY_TIMES = 3

# MONGO_URI = 'mongodb://localhost:27017'
# MONGO_DATABASE = 'sivji-sandbox'


# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# FEED = 'json'

FEED_EXPORT_ENCODING = 'utf-8'

DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 30

RANDOMIZE_DOWNLOAD_DELAY = True

REACTOR_THREADPOOL_MAXSIZE = 128

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 0.25
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 128
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True
RETRY_ENABLED = True

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


################################################################
# PROXY SETTINGS
################################################################
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429]
# 

# PROXY_LIST = get_proxy()

USER_AGENT = get_user_agent('random')

# PROXY_MODE = 0
# USE_PROXY = True
# CHANGE_PROXY_AFTER = 10

DOWNLOADER_MIDDLEWARES = {
    'lazy_crawler.crawler.middlewares.CrawlerSpiderMiddleware': 400,
    'lazy_crawler.crawler.middlewares.RandomUserAgentMiddleware': 120,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 80,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 130,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 900,
    # 'scraper.middlewares.ScraperDownloaderMiddleware': 1000
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'scrapy_proxies.RandomProxy': 80,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

