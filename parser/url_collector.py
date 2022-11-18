import concurrent.futures
import time

from lxml import etree
import requests

from data_collector import DataCollector
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for page in range(1, 2):
                url = f'https://www.kijiji.ca/b-apartments-condos/' \
                      f'city-of-toronto/page-{page}/c37l1700273'
                executor.submit(self.get_url_from_page, page_url=url)
        logger.info(msg=f"{len(self.all_urls)} urls collected")
