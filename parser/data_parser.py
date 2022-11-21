from datetime import datetime
import json
import logging

from lxml import etree

from database.db_saver import DBSaver


class DataParser:
    def __init__(self, list_of_sources):
        self.list_of_sources = list_of_sources
        self.source = None
        self.source_json = None
        self.apart_info = {}
        self.apart_details = {}
        self.owner_details = {}
        self.phone_number = None
        self.parsing()

    def id(self):
        return int(self.source.xpath('//a[@aria-current="page"]/text()')[0])

    def title(self):
        return self.source.xpath('(//h1/text())')[0]

    def city(self):
        return self.source.xpath('//span[@class="text-3814801860"]/text()')[0]

    def location(self):
        return self.source.xpath('//span[@class="address-'
                                 '3617944557"]/text()')[0]

    def price_currency(self):
        pr_cur = self.source.xpath('//div[@class="priceWrapper-1165431705"]'
                                   '//span/text()')[0]
        if pr_cur[-1].isdigit():
            return int(pr_cur[1:].replace(",", "")), pr_cur[0]
        else:
            return None, None

    def price_description(self):
        return self.source.xpath('//span[@class="utilities-3542420827"]'
                                 '/text()')[0]

    def date_posted(self):
        return str(datetime.strptime(self.source.xpath('//time/@datetime')[1],
                                     "%Y-%m-%dT%H:%M:%S.%fZ"))

    def description(self):
        return " ".join(
            self.source.xpath('//div[@class="descriptionContainer-231909819"]'
                              '//div//child::text()'))

    def utilities(self, key):
        ut_dict = {
            "hydro": ("Utilities Included", "[1]"),
            "heat": ("Utilities Included", "[2]"),
            "water": ("Utilities Included", "[3]"),
            "wi-fi": ("Wi-Fi and More", ""),
            "appliances": ("Appliances", ""),
            "space": ("Personal Outdoor Space", "")
        }
        availability = self.source.xpath(
            f'//h4[contains(text(),"{ut_dict[key][0][1:-2]}")]'
            f'//following-sibling::ul//li{ut_dict[key][1]}/@class')
        return any("available" in text for text in availability)

    def terms(self, key):
        terms_dict = {
            "parking": "Parking Included",
            "agreement_type": "Agreement Type",
            "pet_friendly": "Pet Friendly",
            "size": "Size (sqft)",
            "furnished": "Furnished",
            "ac": "Air Conditioning",
            "int_smoking": "Smoking Permitted"
        }
        terms_text = self.source.xpath(
            f'//dt[text()[contains(.,"{terms_dict[key][1:-2]}")]]'
            f'//following::dd[1]/text()')
        try:
            assert terms_text[0] != "No" and terms_text[0] != "Not Available"
        except (IndexError, AssertionError):
            return False
        else:
            return terms_text[0]

    def move_in_date(self):
        date = self.source.xpath(f'//dt[text()[contains(.,"Move-In Date")]]'
                                 f'//following::dd[1]//span/text()')
        try:
            date[0]
        except IndexError:
            return None
        else:
            return str(datetime.strptime(date[0],
                                         "%B %d, %Y"))

    def owner_id(self):
        own_id = self.source.xpath('//a[@class="link-2686609741"]/@href')[0]
        return int(own_id.split('/')[2])

    def owner_name(self):
        if self.phone_number:
            return self.source_json['config']['profile']['postersCompanyName']
        return self.source_json['viewItemPage']['viewItemData']['sellerName']

    def rank(self):
        return self.source.xpath('(//div[@class="line-2791721720"]'
                                 '/text())[1]')[0]

    def on_kijiji_since(self):
        return self.source_json['config']['profile']['memberSince']

    def collect_data(self):
        self.apart_info = {
            "id": self.id(),
            "title": self.title(),
            "city": self.city(),
            "location": self.location(),
            "price": self.price_currency()[0],
            "currency": self.price_currency()[1],
            "price_description": self.price_description(),
            "date_posted": self.date_posted(),
            "description": self.description(),
            "owner_id": self.owner_id()
        }

        self.apart_details = {
            "apartment_id": self.id(),
            "ut_incl_hydro": self.utilities("hydro"),
            "ut_incl_heat": self.utilities("heat"),
            "ut_incl_water": self.utilities("water"),
            "wi_fi": self.utilities("wi-fi"),
            "parking": int(self.terms("parking")[0]),
            "agreement_type": self.terms("agreement_type"),
            "move_in_date": self.move_in_date(),
            "pet_friendly": bool(self.terms("pet_friendly")),
            "size": int(self.terms("size").replace(",", "") if self.terms(
                "size") else False),
            "unit_furnished": bool(self.terms("furnished")),
            "appliances": self.utilities("appliances"),
            "ac": bool(self.terms("ac")),
            "outdoor_space": bool(self.utilities("space")),
            "smoking": bool(self.terms("int_smoking"))
        }

        self.owner_details = {
            "id": self.owner_id(),
            "name": self.owner_name(),
            "rank": self.rank(),
            "on_kijiji_since": self.on_kijiji_since(),
            "phone": self.phone_number
        }

    def parsing(self):
        for source in self.list_of_sources:
            self.source = etree.HTML(source[0])
            self.source_json = source[1]
            self.phone_number = source[2]
            if self.source is not None:
                self.collect_data()
                with DBSaver() as saver:
                    saver.save(
                        info=self.apart_info,
                        details=self.apart_details,
                        owner=self.owner_details
                    )
                    logging.info(msg="Row added to db")
            else:
                logging.warning(msg="Page is empty")

