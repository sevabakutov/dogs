import os

BOT_NAME = 'scrapy_project'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

DOWNLOAD_DELAY = 2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

ITEM_PIPELINES = {
    'pipelines.save_to_csv.SaveToCSVPipeline': 300,
    'pipelines.dog_pipeline.DogPipeline': 400,
}

DOWNLOADER_MIDDLEWARES = {
    'middlewares.fake_user_agent.ScrapeOpsFakeUserAgentMiddleware': 400,
    'middlewares.retry_middleware.TooManyRequestsRetryMiddleware': 500,
}

SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY', None)