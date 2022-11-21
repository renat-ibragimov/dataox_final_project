import concurrent.futures
import time

from lxml import etree
import requests

from data_collector import DataCollector
from last_page_searcher import cities_urls, last_page
from logger import logger


class UrlCollector:
    def __init__(self):
        self.all_urls = set()
        self.start_collecting()
        DataCollector(self.all_urls)

    def get_url_from_page(self, page_url, timeout=10):
        response = requests.get(url=page_url, timeout=timeout)
        source = etree.HTML(response.text)
        links = source.xpath('//a[@class="title "]/@href')
        if not links:
            time.sleep(0.5)
            return self.get_url_from_page(page_url, timeout=10)
        self.all_urls.update(links)

    def start_collecting(self):
        for city in cities_urls:
            l_page = last_page(city)
            with concurrent.futures.ThreadPoolExecutor(max_workers=25) \
                    as executor:
                for page in range(1, 2):
                    url = cities_urls[city].format(page)
                    executor.submit(self.get_url_from_page, page_url=url)
        logger.info(msg=f"{len(self.all_urls)} urls collected")
