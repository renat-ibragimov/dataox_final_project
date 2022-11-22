import asyncio
import json

import aiohttp
from lxml import etree

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
        self.run_collector()
        DataParser(self.source_to_parse)

    async def get_source_html(self, url: str, session, link):
        async with session.get(url, headers=self.headers) as resp:
            dom = await resp.text()
            source = etree.HTML(dom)
            try:
                js_string = source.xpath(
                    '//div[@id="FesLoader"]//script[@type="text/javascript"]'
                    '/text()')[0].replace("window.__data=", "")[:-1]
            except IndexError:
                return
            self.source_html = dom
            self.source_json = json.loads(js_string)
            logger.info(msg=f'HTML and JSON data collected')
            await self.get_phone_number(session, link)

    async def get_phone_number(self, session, link):
        phone_token = self.source_json.get('config', {})\
            .get('profile', {}).get('phoneToken', {})
        if not phone_token:
            self.phone_num = ''
        else:
            async with session.get(
                    url=f"https://www.kijiji.ca/j-vac-phone-get.json?"
                        f"token={phone_token}", headers=self.headers) as res:
                res_text = await res.text()
                js_obj = json.loads(res_text)
                self.phone_num = js_obj["phone"]
        self.source_to_parse.append((self.source_html,
                                     self.source_json,
                                     self.phone_num))
        self.set_of_links.discard(link)

    async def get_tasks(self):
        tasks = []
        sem = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            while self.set_of_links:
                for link in self.set_of_links:
                    url = f"https://www.kijiji.ca{link}?siteLocale=en_CA"
                    tasks.append(asyncio.ensure_future(
                        self.bound_fetch(sem, url, session, link)))
                await asyncio.gather(*tasks)

    async def bound_fetch(self, sem, url: str, session, link):
        async with sem:
            await self.get_source_html(url, session, link)

    def run_collector(self):
        asyncio.run(self.get_tasks())
