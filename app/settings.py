import os.path
import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
ENCODERS_DIR = os.path.join(DATA_DIR, "encoders")
IMPUTERS_DIR = os.path.join(DATA_DIR, "imputers")
MODELS_DIR = os.path.join(DATA_DIR, "models")
DATASET_DIR = os.path.join(DATA_DIR, "train", "datasets")


env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, "..", ".env"))

SCRAPER_API_KEY = env('SCRAPER_API_KEY')

LOG_FILE = 'scrapy_log.txt'

BOT_NAME = "grayhound"

SPIDER_MODULES = ["app.spiders"]
NEWSPIDER_MODULE = "app.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [502, 503, 504, 522, 524, 408]

DOWNLOAD_DELAY = 2.0
# RANDOMIZE_DOWNLOAD_DELAY = True

SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True



DOWNLOADER_MIDDLEWARES = {
    'utils.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
    'utils.middlewares.TooManyRequestsRetryMiddleware': 500,

}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
