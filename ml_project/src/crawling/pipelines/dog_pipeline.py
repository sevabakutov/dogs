import os
from settings import DATA_DIR
from datetime import datetime
from scrapy.exporters import CsvItemExporter

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