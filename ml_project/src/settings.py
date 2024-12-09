import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ENCODERS_DIR = os.path.join(DATA_DIR, "encoders")
IMPUTERS_DIR = os.path.join(DATA_DIR, "imputers")
MODELS_DIR = os.path.join(DATA_DIR, "models")
DATASET_DIR = os.path.join(DATA_DIR, "train", "datasets")

SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY', None)

BOT_NAME = 'crawling'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [502, 503, 504, 522, 524, 408]

DOWNLOAD_DELAY = 2

SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'middlewares.fake_user_agent.ScrapeOpsFakeUserAgentMiddleware': 400,
    'middlewares.retry_middleware.TooManyRequestsRetryMiddleware': 500,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"