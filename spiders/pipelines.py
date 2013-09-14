# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import os
import time

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JsonExportPipeline(object):
    
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}
    
    def spider_opened(self, spider):
        outpath = os.environ['SCRAPEDUMP']
        
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')
        f = open(outpath + '%s_%s_events.json' % (spider.name, st), 'wb')
        self.files[spider] = f
        self.exporter = JsonItemExporter(f)
        self.exporter.start_exporting()
        
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        f = self.files.pop(spider)
        f.close()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class AlivePipeline(object):
    def process_item(self, item, spider):
        return item
    
# class AlivemagPipeline(object):
#     def process_item(self, item, spider):
#     
#         ## Generate a timestamp
#         ts = time.time()
#         st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')
#         ## TODO: Cleanup
#         fname = st + spider.name
# 
#         fout = open('fname' + '.out', 'w')
#         
#         log.msg("Name: %s \n Date: %s \n Price: %s \n" % (repr(item['name'])[1:-1].lstrip('u'),
#                                                  repr(item['date'])[4:-2],
#                                                  repr(item['price'])[4:-2].split('\\')[0]),
#                                                  level=log.INFO)
#         
#         return item