from scrapy import signals
from scrapy.exporters import CsvItemExporter
import json
from itemadapter import ItemAdapter
import openpyxl
# from openpyxl.utils import get_column_letter
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem
import datetime

class CSVPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open(f'scraped_data_{self.created_time}.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()

    def open_spider(self, spider):
        self.file = open(f'scraped_data_{self.created_time}.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


class ExcelWriterPipeline(object):

    def __init__(self):
        self.created_time = datetime.datetime.now()
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Scraped Data"
        self.row_num = 1  # counter for the current row in the sheet

    def process_item(self, item, spider):
        # Add headings to the sheet if it's the first item
        if self.row_num == 1:
            self.ws.append(list(item.keys())) # convert dict_keys to a list and use it as headings
        # Add the item data to the sheet
        self.ws.append(list(item.values()))
        self.row_num += 1  # increment the row counter
        return ''
        # return item

    def close_spider(self, spider):
        self.wb.save(f"scraped_data_{self.created_time}.xlsx")  # save the workbook