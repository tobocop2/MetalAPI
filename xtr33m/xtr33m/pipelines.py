# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class Xtr33MPipeline(object):
    def process_item(self, item, spider):
        return item



#class ReleasePipeline(object):
#    def process_item(self, item, spider):
#        item['detailed_discography'][release_index][release_name]['songs'][song_index][track_name]['lyrics'] = lyrics
#        if len(item['detailed_discography']) == item['releases']['release_count']:
#            yield item
#        else:
#            raise DropItem("Duplicate item found: %s" % item)
#            return item
