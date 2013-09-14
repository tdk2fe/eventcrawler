import urllib

from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from spiders.items import EventItem


class LaduenewsSpider(BaseSpider):
    name = 'laduenews'
    allowed_domains = ['laduenews.com']


    params = urllib.urlencode({'areaSelect':'',
                               'c[]':'calendar',
                               'd':'',
                               'd1':'09/11/2013',
                               'd2':'09/17/2013',
                               'fl':'',
                               'l':'100',
                               'q':'*',
                               's':'start_time',
                               'sd':'asc',
                               'venue_zip':''
    })
    
    start_urls = ['http://www.laduenews.com/calendar/search/?' + params]
    
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        log.msg("Response URL: %s" % response.url, level=log.INFO)
        events = hxs.select("/html/body/div[3]/div/div[2]/div[4]/div[3]/ol/*")
        item_list = []
        
        for event in events:
            item = EventItem()
            item['name'] = event.select("../li/div/div/h3/a/text()").extract()
            item['price'] = "Not yet available"
            item['date'] = event.select("../li/strong/div/div/span/ul/li/text()").extract()
            item_list.append(item)
            log.msg("Added item %s on date %s\n" % (repr(item.get('name'))[1:-1], repr(item.get('date'))[1:-1]), level=log.INFO)
        return item_list
