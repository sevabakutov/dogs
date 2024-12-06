import json
import scrapy
import settings
from urllib.parse import urlencode
from items.dog import DogItem


class NewRaceSpider(scrapy.Spider):

    name = 'race_spider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'utils.pipelines.DogPipeline': 400,
        }
    }

    def __init__(self, api_key='',  date='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.date = date

    def start_requests(self):
        start_urls = [
            f'https://greyhoundbet.racingpost.com/meeting/blocks.sd?view=meetings&r_date={self.date}&blocks=header%2Clist'
            ]
        for url in start_urls:
            yield scrapy.Request(self.get_proxy_url(url), callback=self.parse)

    
    def get_proxy_url(self, url):
        if not self.api_key:
            raise ValueError("API key has not been set yet")
        payload = {'api_key': self.api_key, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url


    def parse(self, response):
        json_text = response.text
        data = json.loads(json_text)
        meetings = data['list']['items']

        for meeting in meetings:
            races = meeting['races']

            for race in races:
                track_id = race['trackId']
                race_id = race['raceId']
                dist = race['distance']

                url = f'https://greyhoundbet.racingpost.com/card/blocks.sd?track_id={track_id}&race_id={race_id}&r_date={self.date}&tab=form&blocks=card-header%2Ccard-pager%2Ccard-tabs%2Ccard-title%2Cform'

                yield scrapy.Request(
                    self.get_proxy_url(url),
                    callback=self.parse_race,
                    meta={'dist': dist}
                )

    def parse_race(self, response):
        json_text = response.text
        data = json.loads(json_text)

        race_info = data['card-tabs']

        race_date_time = race_info['raceDate']
        race_grade = race_info['raceGrade']
        track = race_info['trackName'].capitalize()

        dogs = data['form']['dogs']

        for dog in dogs:
            item = DogItem()

            item['race_date_time'] = race_date_time
            item['raceClass'] = race_grade
            item['trackName'] = track
            item['name'] = dog['dogName']
            item['forecast'] = dog['forecast']
            item['comments'] = dog['forecastComment']
            item['trapNumber'] = dog['trapNum']
            item['raceDistance'] = response.meta.get('dist')

            forms = dog['forms']

            for i, form in enumerate(forms, 1):
                if i > 5:
                    continue
                item[f'by_{i}'] = form['by']
                item[f'run_time_{i}'] = form['calcRTimes']
                item[f'comnt_{i}'] = form['closeUpCmnt']
                item[f'dist_{i}'] = form['distanceTitle']
                item[f'going_{i}'] = form['goingType']
                item[f'race_grade_{i}'] = form['gradeCde']
                item[f'odds_{i}'] = form['oddsDesc']
                item[f'finished_{i}'] = form['rOutcomeId']
                item[f'sec_time_{i}'] = form['sectionalTime']
                item[f'trap_{i}'] = form['trap']
                item[f'weight_{i}'] = form['weight']

            yield item

        



