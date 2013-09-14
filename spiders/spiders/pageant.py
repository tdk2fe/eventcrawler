from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from spiders.items import EventItem


class PageantSpider(BaseSpider):
    name = 'pageant'
    allowed_domains = ['thepageant.com']
    start_urls = ['http://www.thepageant.com/shows/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        events = hxs.select(".//*/div[@class='wt-list wt-events']/table/tbody/tr/td[2]")
        log.msg("From URL: %s \n Events:" % response.url, events, level=log.INFO)
        item_list = []
        for event in events:
            item = EventItem()
            item['name'] = event.select("../tr[1]/td/a/text()").extract()
            item["date"] = event.select(".//*[@id='wordtour-content']/div/table/tbody/tr[1]/td[2]/b[1]/text()").extract()
            item["price"] = event.select(".//*[@id='wordtour-content']/div/table/tbody/tr[1]/td[2]/text()[4]").extract()
            item_list.append(item)
        return item_list
        
