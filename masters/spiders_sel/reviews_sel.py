from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from masters import settings
from masters.utils import unicode_utils, coordinate_utils
from masters.data_structures.Review import Review


class SeleniumReviewSpider(object):
    def __init__(self, url):
        chrome_options = Options()
        if settings.HEADLESS_MODE:
            chrome_options.add_argument("--headless")
        service_args = ['--verbose']
        driver = webdriver.Chrome(
            chrome_options=chrome_options,
            service_args=service_args)
        driver.get(url)
        driver.implicitly_wait(5)
        self.driver = driver

    def select_all_languages(self):
        self.driver.find_element_by_css_selector('div.choices div.ui_radio label.label').click()
        self.driver.implicitly_wait(3)

    def is_next(self):
        return not (self.get_next_page_url() is "")

    def get_next_page_url(self):
        return unicode_utils.unicode_to_string(
            self.driver.find_element_by_css_selector('div.ui_pagination a.next').get_attribute("href"))

    def get_coordinates(self):
        coord_url = self.driver.find_element_by_css_selector("div.staticMap img").get_attribute("src")
        return coord_url

    def next_page(self):
        self.driver.find_element_by_css_selector('div.ui_pagination a.next').click()
        self.driver.implicitly_wait(2)

    def scrap_page(self):
        review_location_name = unicode_utils.unicode_to_string(
            self.driver.find_element_by_css_selector('div h1.ui_header').get_attribute('text'))
        # review_location_tags = unicode_utils.unicode_list_to_string(
        #     response.css('div.ppr_priv_trip_planner_breadcrumbs').xpath(
        #         '//ul[@class="breadcrumbs"]/li/a/span/text()').extract())
        review_location_description_tags = unicode_utils.unicode_list_to_string(
            self.driver.find_element_by_css_selector('div.headerInfoWrapper div.detail a').get_attribute('text'))
        review_current_page = unicode_utils.unicode_to_string(
            self.driver.find_element_by_css_selector('div.pageNumbers a.current').get_attribute('data-page-number'))

        review_last_page = unicode_utils.unicode_to_string(
            self.driver.find_element_by_css_selector('div.pageNumbers a.last').get_attribute('data-page-number'))

        location_lat, location_lng = coordinate_utils.parse_google_maps_link(self.get_coordinates())
        place_rate = unicode_utils.unicode_to_string(
            self.driver.find_element_by_css_selector('span.overallRating').get_attribute('text'))

        reviews = []

        for review in self.driver.find_elements_by_css_selector("div.review-container"):
            review_id = unicode_utils.unicode_to_string(review.get_attribute("data-reviewid"))
            user_id = unicode_utils.unicode_user_uid_to_string(
                review.find_element_by_css_selector('div.member_info div.memberOverlayLink').get_attribute('id'))
            review_date = unicode_utils.unicode_date_to_string_number(
                review.find_element_by_css_selector('span.ratingDate').get_attribute('title'))
            review_rate = unicode_utils.unicode_rating_to_string(
                review.find_element_by_css_selector('span.ui_bubble_rating').get_attribute('class'))
            username = unicode_utils.unicode_to_string(
                review.find_element_by_css_selector('div.info_text div').get_attribute('text'))
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
            self.save_to_file(reviews, review_location_name ,review_current_page)

    @staticmethod
    def save_to_file(reviews, location_name, current_page):
        filename = 'data/data_reviews/reviews-%s-%s.csv' % (location_name, current_page)
        with open(filename, 'wb') as f:
            f.write(Review.get_csv_header())
            for review in reviews:
                f.write(review.get_csv_line())
        print('Saved file %s' % filename)
        # self.log('Saved file %s' % filename)


# todo iterate over reviews and parse them as with scrapy parser
# todo scrap page and save it to file


def scrap_reviews(url):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    service_args = ['--verbose']

    driver = webdriver.Chrome(
        chrome_options=chrome_options,
        service_args=service_args
    )
    driver.get(url)
    driver.implicitly_wait(3)

    driver.find

    coord_url = driver.find_element_by_css_selector("div.staticMap img").get_attribute("src")
    print(coord_url)
    driver.close()
    return coord_url


def get_coordinates(url):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

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
