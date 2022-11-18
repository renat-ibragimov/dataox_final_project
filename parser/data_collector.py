import concurrent.futures

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from data_parser import DataParser
from logger import logger


class DataCollector:
    def __init__(self, set_of_links):
        self.set_of_links = set_of_links
        self.list_of_sources = []
        self.start_collecting()
        DataParser(self.list_of_sources)

    def get_page_source(self, link):
        chrome_options = Options()
        chrome_prefs = {"profile.default_content_settings": {"images": 2},
                        "profile.managed_default_content_settings": {
                            "images": 2}}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options,
                                   desired_capabilities=caps)
        browser.get(f' https://www.kijiji.ca{link}')
        # Usable xpathes for buttons and hidden info
        phone_button_xpath = '//button[@class="phoneNumberContainer-' \
                             '69344174 phoneShowNumberButton-1052915314 ' \
                             'button-1997310527 button__medium-1066667140"]'
        phone_number_xpath = '//a[@class="phoneNumberContainer-69344174"]'
        description_button_xpath = '//div[@class="showMoreWrapper-' \
                                   '1159407536 showMoreWrapper__newRentals-' \
                                   '1768917462"]//child::button'
        full_descr = '//div[@class="descriptionContainer-231909819"]//div'

        wait = WebDriverWait(browser, 5)

        # Opening hidden info
        try:
            wait.until(ec.element_to_be_clickable(
                (By.XPATH, description_button_xpath)))
        except TimeoutException:
            pass
        else:
            descr_button = browser.find_element(By.XPATH,
                                                description_button_xpath)
            browser.execute_script("arguments[0].click();", descr_button)

        try:
            wait.until(
                ec.element_to_be_clickable((By.XPATH, phone_button_xpath)))
        except TimeoutException:
            pass
        else:
            ph_button = browser.find_element(By.XPATH, phone_button_xpath)
            browser.execute_script("arguments[0].click();", ph_button)

        try:
            wait.until(
                ec.presence_of_element_located((By.XPATH, phone_number_xpath)))
        except TimeoutException:
            pass

        try:
            wait.until(ec.presence_of_element_located((By.XPATH, full_descr)))
        except TimeoutException:
            logger.warning(msg=f"REPEATED REQUEST: {link}")
            return self.get_page_source(link)

        self.list_of_sources.append(browser.page_source)
        logger.info(msg="Page data collected")

    def start_collecting(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for link in self.set_of_links:
                executor.submit(self.get_page_source, link=link)
        logger.info(msg=f'{len(self.list_of_sources)} pages '
                            f'data collected')
