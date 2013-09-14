from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from spiders.items import EventItem


class AliveSpider(CrawlSpider):
    name = 'alive'
    allowed_domains = ["alivemag.com"]
    start_urls = ["http://www.alivemag.com/events/sub_events_results.cfm"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('sub_events_results\.cfm\?startRow=',),
            deny=('sub_events_results\.cfm\?startRow=1',)), callback='parse_page'),
    )
    
    def parse_page(self, response):
        log.msg('Parsing page URL: %s\n' % response.url, level=log.INFO)
        hxs = HtmlXPathSelector(response)
        events = hxs.select(".//*[@id='main']/div/p[position() > 2]")
        item_list = []
        for event in events:
            item = EventItem()
            item['name'] = event.select("strong/a/text()").extract()
            item['date'] = event.select("strong[2]/following-sibling::text()[1]").extract()
            item['price'] = event.select("strong[4]/following-sibling::text()[1]").extract()
            item_list.append(item)
            log.msg("Added new item to list: %s" % repr(item.get('name'))[1:-1], level=log.INFO)
            # log.msg("Name: %s Date: %s Price %s" % (repr(item['name'])[1:-1].lstrip('u')[1:-1].rstrip("\\t").rstrip("\\n"), item['date'], item['price']), level=log.INFO)
        return item_list

        
