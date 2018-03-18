# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.exporters import JsonItemExporter

class SpiderdemoPipeline(object):
    def process_item(self, item, spider):
        return item
# 自定义存JSON
# class JsonWithEncodingPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('demo.json', 'w+', encoding='utf-8')
#         self.file.write("[")
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#         self.file.write(line)
#         return item
#     def spider_closed(self, spider):
#     	# last_line = self.file.readlines()[-1][:-1]
    	
#         self.file.write("]")
#         self.file.close()

# 使用内置JsonItemExporter
class JsonWithEncodingPipeline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        #打开一个json文件
        self.file = codecs.open('demo.json', 'w+', encoding='utf-8')
        #创建一个exporter实例,入参分别是下面三个，类似前面的自定义导出json
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        #开始导出
        self.exporter.start_exporting()
    def close_spider(self,spider):
        #完成导出
        self.exporter.finish_exporting()
        #关闭文件
        self.file.close()
    #最后也需要调用process_item返回item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item