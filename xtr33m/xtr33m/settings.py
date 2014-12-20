# -*- coding: utf-8 -*-

# Scrapy settings for xtr33m project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xtr33m'

SPIDER_MODULES = ['xtr33m.spiders']
NEWSPIDER_MODULE = 'xtr33m.spiders'
COOKIES_ENABLED = 0
#DOWNLOAD_DELAY = 0.25
DOWNLOAD_DELAY = 0
LOG_FILE = 'bands.txt'
#LOG_STDOUT = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xtr33m (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'xtr33m.rotate_useragent.RotateUserAgentMiddleware' :400
        }
