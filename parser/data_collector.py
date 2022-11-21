import json

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
            js_string = source.xpath(
                '(//div[@id="FesLoader"]//script[@type="text/javascript"]'
                '/text()')[0].replace("window.__data=", "")[:-1]
            self.source_html = res.text
            self.source_json = json.loads(js_string)

            logger.info(msg=f'HTML and JSON data collected')
            logger.info(msg=f"{js_string}")
            self.get_phone_number()

    def get_phone_number(self):
        try:
            phone_token = self.source_json['config']['profile']['phoneToken']
        except KeyError:
            self.phone_num = ''
            return
        else:
            with requests.Session() as session:
                res = session.get(f"https://www.kijiji.ca"
                                  f"/j-vac-phone-get.json?token={phone_token}",
                    headers=self.headers)
                self.phone_num = res.json()["phone"]
                logger.info(msg=f'{res.json()["phone"]}')
        finally:
            self.source_to_parse.append(
                (self.source_html, self.source_json, self.phone_num))

    def start_collecting(self):
        for link in self.set_of_links:
            self.get_source_html(link)


d = DataCollector({
                      "/v-apartments-condos/city-of-toronto/furnished-condo-1-1-for-rent-amazing-lake-view/1640293209"})
