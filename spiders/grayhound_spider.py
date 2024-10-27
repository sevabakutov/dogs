import json
import scrapy
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from grayhound.items import GrayhoundItem
from urllib.parse import urlencode


count = 1

class GrayhoundSpider(scrapy.Spider):

    name = "grayhound_spider"

    custom_settings = {
        'ITEM_PIPELINES': {
            'grayhound.app.pipelines.SaveToCSVPipeline': 350,
        },
    }

    def __init__(self, dates=[], api_key='', *args, **kwargs):
        self.logger.debug(f"Initializing GrayhoundSpider with dates: {dates} and api_key: {api_key}")
        super().__init__(*args, **kwargs)
        self.dates = dates
        self.api_key = api_key
        

    def start_requests(self):
        start_urls = []

        for date in self.dates:
            url_first_page = f"https://api.gbgb.org.uk/api/results?page=1&itemsPerPage=100&date={date}&race_type=race"
            url_second_page = f"https://api.gbgb.org.uk/api/results?page=2&itemsPerPage=100&date={date}&race_type=race"

            self.logger.debug(f"Generated URL for date {date}: {url_first_page} and {url_second_page}")

            start_urls.append(url_first_page)
            start_urls.append(url_second_page)
            
        for url in start_urls:
            global count
            self.logger.info(f"Starting request for URL (number {count}): {url}")
            count += 1
            yield scrapy.Request(self.get_proxy_url(url), callback=self.parse)


    def get_proxy_url(self, url):
        if not self.api_key:
            self.logger.error("API key has not been set yet")
            raise ValueError("API key has not been set yet")
        payload = {'api_key': self.api_key, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        self.logger.debug(f"Proxy URL generated: {proxy_url}")
        return proxy_url
    

    def parse(self, response):
        self.logger.debug(f"Parsing response from {response.url}")

        json_text = response.text
        data = json.loads(json_text)
        races = data['items']

        for race in races:
            meeting_id = race['meetingId']
            next_page_url = 'https://api.gbgb.org.uk/api/results/meeting/' + str(meeting_id) + '?meeting=' + str(meeting_id)
            yield scrapy.Request(
                url=self.get_proxy_url(next_page_url),
                callback=self.parse_meeting_page
            )

    def parse_meeting_page(self, response):
        self.logger.debug(f"Parsing meeting page from {response.url}")

        json_text = response.text
        data = json.loads(json_text)

        item = GrayhoundItem()

        item['raceDate'] = data[0]['meetingDate']
        item['meetingId'] = data[0]['meetingId']
        item['trackName'] = data[0]['trackName']

        races = data[0]['races']

        for race in races:
            item['raceTime'] = race.get('raceTime')
            item['raceId'] = race.get('raceId')
            item['raceNumber'] = race.get('raceNumber')
            item['raceType'] = race.get('raceType')
            item['raceHandicap'] = race.get('raceHandicap')
            item['raceClass'] = race.get('raceClass')
            item['raceDistance'] = race.get('raceDistance')
            item['racePrizes'] = race.get('racePrizes')
            item['raceGoing'] = race.get('raceGoing')
            item['raceForecast'] = race.get('raceForecast')
            item['raceTricast'] = race.get('raceTricast')

            traps = race['traps'] 

            for trap in traps:
                item['trapNumber'] = trap.get('trapNumber')
                item['trapHandicap'] = trap.get('trapHandicap')

                item['dogId'] = trap.get('dogId')
                item['dogName'] = trap.get('dogName')
                item['dogSire'] = trap.get('dogSire')
                item['dogBorn'] = trap.get('dogBorn')
                item['dogColour'] = trap.get('dogColour')
                item['dogSex'] = trap.get('dogSex')
                item['dogSeason'] = trap.get('dogSeason')

                item['trainerName'] = trap.get('trainerName')
                item['ownerName'] = trap.get('ownerName')

                item['SP'] = trap.get('SP')
                item['resultPosition'] = trap.get('resultPosition')
                item['resultMarketPos'] = trap.get('resultMarketPos')
                item['resultMarketCnt'] = trap.get('resultMarketCnt')
                item['resultPriceNumerator'] = trap.get('resultPriceNumerator')
                item['resultPriceDenominator'] = trap.get('resultPriceDenominator')
                item['resultBtnDistance'] = trap.get('resultBtnDistance')
                item['resultSectionalTime'] = trap.get('resultSectionalTime')
                item['resultComment'] = trap.get('resultComment')
                item['resultRunTime'] = trap.get('resultRunTime')
                item['resultDogWeight'] = trap.get('resultDogWeight')
                item['resultAdjustedTime'] = trap.get('resultAdjustedTime')

                yield item






