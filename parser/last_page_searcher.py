import asyncio

import aiohttp
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
headers = {"Accept-Language": "en-US,en;q=0.5",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}


async def get_last_page(url: str, session, city):
    async with session.get(url, headers=headers) as resp:
        dom = await resp.text()
        source = etree.HTML(dom)
        total_cards = source.xpath('//span[@class="resultsShowingCount-'
                                   '1707762110"]/text()')
        try:
            page = int(int(total_cards[0].split("of")[1].replace("results", "")
                           .strip()) / 40)
        except IndexError:
            return
        logger.info(msg=f"{page} pages collected for {city}")
        cities_urls.pop(city)


async def get_tasks():
    tasks = []
    sem = asyncio.Semaphore(4)
    async with aiohttp.ClientSession() as session:
        while cities_urls:
            for city in cities_urls:
                url = f'{cities_urls[city].format(1)}'
                tasks.append(asyncio.ensure_future(
                    bound_fetch(sem, url, session, city)))
            await asyncio.gather(*tasks)


async def bound_fetch(sem, url: str, session, city):
    async with sem:
        await get_last_page(url, session, city)


def run_collector():
    asyncio.run(get_tasks())

run_collector()