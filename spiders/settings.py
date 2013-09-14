# Scrapy settings for alive project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#


LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'alivemag (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
    'crawlers.pipelines.JsonExportPipeline',
]
