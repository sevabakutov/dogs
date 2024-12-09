from settings import SCRAPER_API_KEY
from datetime import datetime
from crawling.spiders.race_spider import NewRaceSpider
from scrapy.crawler import CrawlerProcess

def start_race_spider() -> None:
    date = datetime.today()
    date = date.strftime('%Y-%m-%d')

    grayhound_process = CrawlerProcess()
    grayhound_process.crawl(NewRaceSpider, api_key=SCRAPER_API_KEY, date=date)
    grayhound_process.start()