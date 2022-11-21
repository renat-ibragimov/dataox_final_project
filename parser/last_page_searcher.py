import random
import time

import requests
from lxml import etree

from logger import logger


cities_urls = {
    "Halifax": "https://www.kijiji.ca/b-apartments-condos/"
               "city-of-halifax/page-{}/c37l1700321",
    "Fredericton": "https://www.kijiji.ca/b-apartments-condos/"
                   "fredericton/page-{}/c37l1700018",
    "Winnipeg": "https://www.kijiji.ca/b-apartments-condos/"
                "winnipeg/page-{}/c37l1700192",
    "Victoria": "https://www.kijiji.ca/b-apartments-condos/"
                "victoria-bc/page-{}/c37l1700173",
    "Charlottetown": "https://www.kijiji.ca/b-apartments-condos/"
                     "charlottetown-pei/page-{}/c37l1700119",
    "Regina": "https://www.kijiji.ca/b-apartments-condos/"
              "regina/page-{}/c37l1700196",
    "Edmonton": "https://www.kijiji.ca/b-apartments-condos/"
                "edmonton/page-{}/c37l1700203",
    "St. John's": "https://www.kijiji.ca/b-apartments-condos/"
                  "st-johns/page-{}/c37l1700113",
    "Toronto": "https://www.kijiji.ca/b-apartments-condos/"
               "city-of-toronto/page-{}/c37l1700273",
    "Quebec": "https://www.kijiji.ca/b-appartement-condo/"
              "ville-de-quebec/page-{}/c37l1700124"
}


def last_page(city):
    resp = requests.get(
        f'{cities_urls[city].format(1)}?siteLocale=en_CA',
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/107.0.0.0 Safari/537.36"})
    source = etree.HTML(resp.text)
    total_cards = source.xpath('//span[@class="resultsShowingCount-'
                               '1707762110"]/text()')
    try:
        page = int(int(total_cards[0].split("of")[1].replace("results", "")
                       .strip()) / 40)
    except IndexError:
        time.sleep(random.uniform(1.0, 2.5))
        last_page(city)
        logger.info(msg=f'redirect')
    logger.info(msg=f'Last page for {city} is {page}')
    return page
