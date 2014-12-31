# -*- coding: utf-8 -*-

# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
COOKIES_ENABLED = 0
DOWNLOAD_DELAY = 0.25
RETRY_TIMES = 50
#DOWNLOAD_DELAY = 0
LOG_FILE = 'bands.txt'
#LOG_STDOUT = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraper (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'scraper.rotate_useragent.RotateUserAgentMiddleware' :400
        }
