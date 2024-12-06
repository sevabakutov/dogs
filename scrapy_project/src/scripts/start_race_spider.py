import settings
from datetime import datetime
from spiders.race_spider import NewRaceSpider
from scrapy.crawler import CrawlerProcess

date = datetime.today()
date = date.strftime('%Y-%m-%d')

api_key = settings.SCRAPER_API_KEY

grayhound_process = CrawlerProcess()
grayhound_process.crawl(NewRaceSpider, api_key=api_key, date=date)
grayhound_process.start()
            