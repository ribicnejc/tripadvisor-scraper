from selenium.webdriver.firefox.options import Options
from selenium import webdriver

from masters import settings


def get_gecko_driver():
    gecko_options = Options()
    gecko_options.headless = settings.HEADLESS_MODE

    driver = webdriver.Firefox(options=gecko_options)
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(10)
