import scrapy
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.items import DogItem, GrayhoundItem
from urllib.parse import urlencode


API_KEY = 'f52fd83395bdaecace4c010d4696222d'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class DogSpider(scrapy.Spider):
    name = 'dog_spider'

    def start_requests(self):
        start_urls = [
            "https://api.gbgb.org.uk/api/results/dog/=633184?page=1&itemsPerPage=100&race_type=race",
            ]
        for url in start_urls:
            yield scrapy.Request(get_proxy_url(url), callback=self.parse)


    def parse(self, response):
        json_text = response.text
        data = json.loads(json_text)
        races = data['items']

        for race in races:
            grahound_item = GrayhoundItem()

            grahound_item['name'] = 'Whisky Flyer'

            grahound_item['sp'] = race.get('SP')
            grahound_item['result_position'] = race.get('resultPosition')
            grahound_item['result_btn_distance'] = race.get('resultBtnDistance')
            grahound_item['result_sectional_time'] = race.get('resultSectionalTime')
            grahound_item['result_comment'] = race.get('resultComment')
            grahound_item['result_run_time'] = race.get('resultRunTime')
            grahound_item['result_dog_weight'] = race.get('resultDogWeight')
            grahound_item['result_adjasted_time'] = race.get('resultAdjustedTime')
            grahound_item['trap_number'] = race.get('trapNumber')
            grahound_item['race_time'] = race.get('raceTime')
            grahound_item['race_date'] = race.get('raceDate')
            grahound_item['race_type'] = race.get('raceType')
            grahound_item['race_class'] = race.get('raceClass')
            grahound_item['race_distance'] = race.get('raceDistance')
            grahound_item['race_going'] = race.get('raceGoing')
            grahound_item['race_win_time'] = race.get('raceWinTime')
            grahound_item['track_name'] = race.get('trackName')

            yield grahound_item