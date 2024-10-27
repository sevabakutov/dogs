import os
import logging
from scrapy import signals
from datetime import datetime
from scrapy.exporters import CsvItemExporter

from app.settings import DATA_DIR

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class SaveToCSVPipeline:
    def open_spider(self, spider):
        self.files = {}

    def close_spider(self, spider):
        for file in self.files.values():
            file.finish_exporting()

    def _create_file(self, date) -> str:
        day, month, year = self._parse_date(date)
        newpath = os.path.join(DATA_DIR, "train", str(year), str(month))
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        file_path = os.path.join(newpath, f'{day}.csv')
        return file_path

    def _parse_date(self, date):
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        return (date_obj.day, date_obj.month, date_obj.year)
    

    def _exporter_for_item(self, item):
        date = item['raceDate']
        file_path = self._create_file(date)

        if file_path not in self.files:
            file = open(file_path, mode='ab')
            exporter = CsvItemExporter(file)
            exporter.start_exporting()
            self.files[file_path] = exporter
        return self.files[file_path]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
    
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.open_spider, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.close_spider, signal=signals.spider_closed)
        return pipeline


        


class DogPipeline:

    def _get_file_path(self):
        dir_path = os.path.join(DATA_DIR, "to_pred")
        os.makedirs(dir_path, exist_ok=True)
        date = datetime.today()
        date = date.strftime('%Y-%m-%d')
        file_name = f'to_pred_{date}.csv'
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def open_spider(self, spider):
        self.file = open(self._get_file_path(), mode='ab')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.file.flush()
        return item

print(os.getcwd())