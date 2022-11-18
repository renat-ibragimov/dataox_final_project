import logging

from lxml import etree
import json
from datetime import datetime


class DataParser:
    def __init__(self, list_of_sources):
        self.list_of_sources = list_of_sources
        self.source = None
        self.apart_info = {}
        self.apart_details = {}
        self.owner_details = {}

        self.parsing()
        self.save_to()

    def id(self):
        return self.source.xpath('//a[@aria-current="page"]/text()')[0]

    def title(self):
        return self.source.xpath('(//h1/text())')[0]

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
                                     "%Y-%m-%dT%H:%M:%S.%fZ"))  # TODO change to datetime

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
                                         "%B %d, %Y"))  #  TODO change to datetime

    def owner_title(self):
        return self.source.xpath('//a[@class="link-2686609741"]/text()')[0]

    def rank(self):
        return self.source.xpath('(//div[@class="line-2791721720"]'
                                 '/text())[1]')[0]

    def on_kijiji_since(self):
        on_kijiji_src = self.source.xpath(
            '//span[@class="date-862429888"]/text()')
        try:
            on_kijiji_src[0]
        except IndexError:
            return self.source.xpath(
                '(//div[@class="text-910784403"])[3]/text()')[0]
        else:
            return on_kijiji_src[0]

    def phone_number(self):
        ph_num = self.source.xpath(
            '//a[@class="phoneNumberContainer-69344174"]/@aria-label')
        try:
            ph_num[0]
        except IndexError:
            return "N/A"
        else:
            return ph_num[0].split(":")[1].strip()

    def collect_data(self):
        self.apart_info = {
            "id": self.id(),
            "title": self.title(),
            "location": self.location(),
            "price": self.price_currency()[0],
            "currency": self.price_currency()[1],
            "price_description": self.price_description(),
            "date_posted": self.date_posted(),
            "description": self.description()
        }

        self.apart_details = {
            "overview_ut_incl_hydro": self.utilities("hydro"),
            "overview_ut_incl_heat": self.utilities("heat"),
            "overview_ut_incl_water": self.utilities("water"),
            "overview_wi_fi": self.utilities("wi-fi"),
            "overview_parking": int(self.terms("parking")[0]),
            "overview_agreement_type": self.terms("agreement_type"),
            "overview_move_in_date": self.move_in_date(),
            "overview_pet_friendly": bool(self.terms("pet_friendly")),
            "unit_size": int(self.terms("size").replace(",", "") if self.terms(
                "size") else False), "unit_furnished": self.terms("furnished"),
            "unit_appliances": self.utilities("appliances"),
            "unit_ac": bool(self.terms("ac")),
            "unit_outdoor_space": bool(self.utilities("space")),
            "int_smoking": bool(self.terms("int_smoking"))
        }

        self.owner_details = {
            "owner_title": self.owner_title(),
            "rank": self.rank(),
            "on_kijiji_since": self.on_kijiji_since(),
            "phone": self.phone_number()
        }

    def parsing(self):
        for source in self.list_of_sources:
            self.source = etree.HTML(source)
            if self.source is not None:
                self.collect_data()
            else:
                logging.warning(msg="Page is empty")

    def save_to(self):
        with open("test.txt", "a") as f:
            f.write(f'Apartment Info: {self.apart_info},'
                    f'Apartment Details: {self.apart_details},'
                    f'Owner Details: {self.owner_details}\n')
