import json
import random
import time

from lxml import etree
import requests


from parser.data_parser import DataParser
from parser.logger import logger


class DataCollector:
    def __init__(self, set_of_links):
        self.headers = {"Accept-Language": "en-US,en;q=0.5",
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/107.0.0.0 Safari/537.36"}
        self.set_of_links = set_of_links
        self.source_html = None
        self.source_json = None
        self.phone_num = None
        self.source_to_parse = []
        self.start_collecting()
        DataParser(self.source_to_parse)

    def get_source_html(self, link):
        with requests.Session() as session:
            res = session.get(f"https://www.kijiji.ca{link}?siteLocale=en_CA",
                              headers=self.headers)
            source = etree.HTML(res.text)
            try:
                js_string = source.xpath(
                    '//div[@id="FesLoader"]//script[@type="text/javascript"]'
                    '/text()')[0].replace("window.__data=", "")[:-1]
            except IndexError:
                time.sleep(random.uniform(2.0, 10.0))
                self.get_source_html(link)
                logger.info(msg="Redirect")
                return
            self.source_html = res.text
            self.source_json = json.loads(js_string)
            logger.info(msg=f'HTML and JSON data collected')
            self.get_phone_number()

    def get_phone_number(self):
        phone_token = self.source_json.get('config', {})\
            .get('profile', {}).get('phoneToken', {})
        if not phone_token:
            self.phone_num = ''
        else:
            with requests.Session() as session:
                res = session.get(f"https://www.kijiji.ca"
                                  f"/j-vac-phone-get.json?token={phone_token}",
                                  headers=self.headers)
                self.phone_num = res.json()["phone"]
                logger.info(msg=f'{res.json()["phone"]}')
        self.source_to_parse.append((self.source_html,
                                     self.source_json,
                                     self.phone_num))

    def start_collecting(self):
        for link in self.set_of_links:
            self.get_source_html(link)

# DataCollector({'/v-apartments-condos/city-of-toronto/new-renovated-1-bedroom-apartment-call-today/1631151000'})
