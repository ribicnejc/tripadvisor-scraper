import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from masters import settings
from masters.utils.logger_utils import Logger
from masters.utils.timer_utils import Timer
from masters.utils import unicode_utils, coordinate_utils
from masters.data_structures.Review import Review


def stale_decorator(f):
    def wrapper(*args, **kwargs):
        counter = 10
        while counter != 0:
            try:
                result = f(*args, **kwargs)
                return result
            except StaleElementReferenceException:
                Logger.log_it("Stale element... retrying")
                counter -= 1
            except WebDriverException:
                Logger.log_it("Web driver exception... retrying")
                counter -= 1
        return None

    return wrapper


class SeleniumReviewSpider(object):
    def __init__(self, url):
        Logger.log_it("##########################################")
        self.timer = Timer()
        self.timer.start_timer()
        chrome_options = Options()
        if settings.HEADLESS_MODE:
            chrome_options.add_argument("--headless")
        service_args = ['--verbose']
        # driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        driver = webdriver.Chrome(
            chrome_options=chrome_options,
            service_args=service_args)
        # driver.add_cookie({'name': 'TALanguage', 'value': 'ALL'})
        driver.get(url)
        driver.implicitly_wait(2)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    @stale_decorator
    def select_all_languages(self):
        time.sleep(1)
        all_languages = self.driver.find_element_by_xpath('//div[@data-value="ALL"]')
        all_languages.click()
        time.sleep(1)
        self.driver.implicitly_wait(2)

    @stale_decorator
    def is_all_languages_selected(self):
        all_languages = self.driver.find_element_by_xpath('//input[@id="filters_detail_language_filterLang_ALL"]')
        return all_languages.is_selected()

    @stale_decorator
    def has_next_review_page(self):
        Logger.log_it("Checking if next page exists...")
        return not (self.get_next_page_url() is None)

    @stale_decorator
    def get_next_page_url(self):
        Logger.log_it("Retrieving next page url...")
        next_url = self.driver.find_element_by_css_selector('div.ui_pagination a.next').get_attribute("href")
        f = lambda x: "None" if next_url is None else next_url
        Logger.log_it("Next url: " + f(next_url))
        return next_url

    @stale_decorator
    def get_coordinates(self):
        coord_url = self.driver.find_element_by_css_selector("div.staticMap img").get_attribute("src")
        return coord_url

    @stale_decorator
    def next_page(self):
        try:
            if not self.is_all_languages_selected():
                Logger.log_it("All language not selected... selecting all language")
                self.select_all_languages()
            self.driver.find_element_by_css_selector('div.ui_pagination a.next').click()
        except WebDriverException:
            Logger.log_it("There is no more pages!")
        self.driver.implicitly_wait(2)

    @stale_decorator
    def scrap_page(self):
        self.driver.implicitly_wait(2)
        time.sleep(1)
        review_location_name = self.driver.find_element_by_css_selector('div h1.ui_header').text
        review_location_description_tags = self.driver.find_element_by_css_selector(
            'div.headerInfoWrapper div.detail a').text
        review_current_page = self.driver.find_element_by_css_selector('div.pageNumbers a.current').get_attribute(
            'data-page-number')
        review_last_page = self.driver.find_element_by_css_selector('div.pageNumbers a.last').get_attribute(
            'data-page-number')
        location_lat, location_lng = coordinate_utils.parse_google_maps_link_selenium(self.get_coordinates())
        place_rate = self.driver.find_element_by_css_selector('span.overallRating').text

        reviews = []
        for review in self.driver.find_elements_by_css_selector("div.review-container"):
            review_id = review.get_attribute("data-reviewid")
            user_id = review.find_element_by_css_selector('div.member_info div.memberOverlayLink').get_attribute('id')
            review_date = review.find_element_by_css_selector('span.ratingDate').get_attribute('title')
            review_rate = review.find_element_by_css_selector('span.ui_bubble_rating').get_attribute('class')
            username = review.find_element_by_css_selector('div.info_text div').text
            review_data = Review(review_location_name,
                                 review_location_description_tags,
                                 location_lat,
                                 location_lng,
                                 review_id,
                                 review_date,
                                 user_id,
                                 place_rate,
                                 review_rate,
                                 username)
            reviews.append(review_data)
        self.save_to_file(reviews, review_location_name, review_current_page, review_last_page)

    def stop_spider(self):
        Logger.log_it("-------------------------------------------")
        self.driver.close()
        self.timer.stop_timer()
        Logger.log_it(self.timer.print_time())



#je all ... potem je eng... klikne in se uganse!!!

    @staticmethod
    def save_to_file(reviews, location_name, current_page, last_page):
        filename = 'data/data_reviews/selenium_reviews-%s-%s-%s.csv' % (location_name, current_page, last_page)
        with open(filename, 'w') as f:
            f.write(Review.get_csv_header())
            for review in reviews:
                f.write(review.get_csv_line())

        Logger.log_it('Saved file %s' % filename)


def get_coordinates(url):
    chrome_options = Options()
    if settings.HEADLESS_MODE:
        chrome_options.add_argument("--headless")
    # chrome_options.binary_location = '/opt/google/chrome/google-chrome'
    # service_log_path = "{}/chromedriver.log".format("/home/nejc/Desktop/scrapers/trip/")
    service_args = ['--verbose']

    driver = webdriver.Chrome(
        chrome_options=chrome_options,
        service_args=service_args,
        # service_log_path=service_log_path
    )
    driver.get(url)
    driver.implicitly_wait(5)

    # Select all languages
    driver.find_element_by_css_selector('div.choices div.ui_radio label.label').click()

    driver.implicitly_wait(3)

    coord_url = driver.find_element_by_css_selector("div.staticMap img").get_attribute("src")
    print(coord_url)
    driver.close()
    return coord_url
