import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from app.service.Scraper.model.TickerInfo import TickerInfo
from app.service.Logger import LoggerSingleton as logger_singleton
from app.service.FakeUserAgent import FakeUserAgent as FakeUserAgentService

class GenericScraper:
    def __init__(self) -> None:
        self.url = "https://statusinvest.com.br/"
        options = webdriver.ChromeOptions()

        options.add_argument(f"user-agent={FakeUserAgentService().get_random_user_agent()}")

        try: 
            self.driver = webdriver.Remote(
                command_executor=os.getenv('SELENIUM_HUB_URL', 'http://selenium-hub:4444'),
                options=options
            )
            self.driver_is_running = True
        except Exception as e:
            self.driver_is_running = False

    def check_driver_is_running(self):
        return self.driver_is_running
    
    def __close_ads(self):
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                self.driver.switch_to.frame(iframe)
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.a_d__v_e__r_t__i_s__i_n__g button"))
                    )
                    element.click()
                    break
                except TimeoutException:
                    self.driver.switch_to.default_content()
                    continue
            self.driver.switch_to.default_content()
        except TimeoutException:
            logger_singleton.print("Anúncio não encontrado ou tempo limite atingido.")

    def call_url(self, url: str) -> None:
        self.driver.get(url)
        self.driver.implicitly_wait(2)
        self.__close_ads()
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def get_data(self, ticker: str) -> TickerInfo:
        return self.get_data_from_ticker(ticker)

    def __del__(self):
        if self.driver_is_running:
            self.driver_is_running = False
            self.driver.quit()
