import scrapy
import re
import json
import time
import functools

from scrapy_splash import SplashRequest

from masters.data_structures.Review import Review
from masters.gecko_spiders import reviews_gecko
from masters.utils import unicode_utils, coordinate_utils, file_utils
from os import listdir


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    root_url = 'https://www.tripadvisor.com'
    current_review_coordinates = ""
    urls = []
    parent_url = ""

    def __init__(self, location='', **kwargs):
        print(location)
        self.parent_url = location
        self.start_time = time.time()
        self.urls.append(location)
        self.scraped_pages = 0
        super(ReviewsSpider, self).__init__(**kwargs)

    def request(self, url, callback):
        request_with_cookies = scrapy.Request(
            url=(self.root_url + url),
            callback=callback)
        return request_with_cookies

    # request_with_cookies.cookies['TALanguage'] = 'ALL'
    # request_with_cookies.cookies[
    #     'TAReturnTo'] = '%1%%2FAttraction_Review%3FreqNum%3D1%26isLastPoll%3Dfalse%26filterLang%3DALL%26filterSegment%3D%26changeSet%3DREVIEW_LIST%26g%3D644300%26q%3D%26t%3D%26puid%3DXExNFQokH20AAYnnbnQAAACo%26preferFriendReviews%3DFALSE%26trating%3D%26d%3D7289577%26filterSeasons%3D%26waitTime%3D19%26paramSeqId%3D10'
    # request_with_cookies.headers[
    #     'User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/71.0.3578.89 Mobile/15E148 Safari/605.1'

    def splash_request(self, url, callback):
        # splash
        return SplashRequest(self.root_url + url, callback, args={
            # optional; parameters passed to Splash HTTP API
            'wait': 10,
            # 'url' is prefilled from request url
            # 'http_method' is set to 'POST' for POST requests
            # 'body' is set to request body for POST requests
        }, )

    def start_requests(self):
        for url in self.urls:
            # self.current_review_coordinates = reviews_gecko.get_coordinates(self.root_url + url)
            # yield self.splash_request(url, self.parse)
            yield self.request(url, self.parse)

    def parse(self, response):
        self.scraped_pages = self.scraped_pages + 1
        next_href = response.css('div.ui_pagination a.next::attr(href)').extract_first()
        if next_href is not None:
            next_review_page_url = unicode_utils.unicode_to_string(next_href)
        else:
            next_review_page_url = ""
        review_location_name = unicode_utils.unicode_to_string(
            response.css('div h1.ui_header::text').extract_first())
        current_url = response.request.url
        current_url = current_url.replace(self.root_url, "")
        if review_location_name is None:
            print("Retrying(1) " + current_url)
            yield self.request(current_url, self.parse)
            return
        # review_location_description_tags = unicode_utils.unicode_list_to_string(
        #     response.css('div.update-wrapper a::text').extract())
        review_current_page = unicode_utils.unicode_to_string(
            response.css('div.pageNumbers span.current::text').extract_first())
        if review_current_page is None:
            print("Retrying(2)" + current_url)
            yield self.request(current_url, self.parse)
            return
        review_last_page = unicode_utils.unicode_list_to_string(
            response.css('div.pageNumbers a.pageNum::text').extract()[-1:])
        review_location_type = unicode_utils.unicode_list_to_string(
            response.css('div._3RTCF0T0 a._1cn4vjE4::text').extract())
        review_location_breadcrumbs = unicode_utils.unicode_list_to_string(
            response.css('div ul.breadcrumbs li.breadcrumb a span::text').extract())
        review_location_rate = unicode_utils.unicode_rating_to_string(
            response.css('div._1NKYRldB span.ui_bubble_rating::attr(class)').extract_first())

        pattern = re.compile(r"(?<=recentHistoryList', )(.*)(?=\);)")
        tripadvisor_data = response.xpath('//script[contains(., "coords")]/text()').re(pattern)[0]
        tripadvisor_data = json.loads(tripadvisor_data)
        location_lat, location_lng = coordinate_utils.parse_json_to_coords(tripadvisor_data)

        location_parent_id = str(tripadvisor_data[0]['details']['parent_id'])
        location_parent_name = str(tripadvisor_data[0]['details']['parent_name'])
        location_grandparent_id = str(tripadvisor_data[0]['details']['grandparent_id'])
        location_grandparent_name = str(tripadvisor_data[0]['details']['grandparent_name'])
        location_full_ids = unicode_utils.unicode_int_list_to_string(tripadvisor_data[0]['details']['parent_ids'])

        reviews = []
        for review in response.css('div.main_content div.Dq9MAugU'):
            review_id = unicode_utils.unicode_to_string(
                review.css('::attr(data-reviewid)').extract_first())

            review_date = unicode_utils.unicode_date_v2_to_string_number(
                review.css('div._2fxQ4TOx span::text').extract_first())

            try:
                review_experience_date = unicode_utils.unicode_date_v3_to_string_number(
                    review.css('div._27JpaCjl span::text').extract()[1])
            except IndexError:
                review_experience_date = review_date

            review_rate = unicode_utils.unicode_rating_to_string(
                review.css('span.ui_bubble_rating::attr(class)').extract_first())

            user_name = unicode_utils.unicode_to_string(review.css('a.ui_header_link::text').extract_first())
            user_link = unicode_utils.unicode_to_string(review.css('a.ui_header_link::attr(href)').extract_first())
            user_id = unicode_utils.unicode_string_to_md5(user_link)

            review_data = Review(review_location_name,
                                 review_current_page,
                                 review_last_page,
                                 review_location_type,
                                 review_location_breadcrumbs,
                                 review_location_rate,
                                 location_lat,
                                 location_lng,
                                 location_parent_id,
                                 location_parent_name,
                                 location_grandparent_id,
                                 location_grandparent_name,
                                 location_full_ids,
                                 review_id,
                                 review_date,
                                 review_experience_date,
                                 review_rate,
                                 user_name,
                                 user_link,
                                 user_id,
                                 self.parent_url)
            reviews.append(review_data)

        if review_location_name is not None:
            review_location_name = review_location_name.replace("/", "").replace(",", "").replace(" ", "_")
        if review_current_page is not None:
            review_current_page = review_current_page.replace("/", "")

        if review_current_page == '1':
            last_scraped_page_url = file_utils.get_last_scraped_page_url(review_location_name, current_url)
            if last_scraped_page_url is not None:
                next_review_page_url = last_scraped_page_url

        filename = 'scraped_data/data_reviews/reviews-%s-%s.csv' % (review_location_name, review_current_page)
        with open(filename, 'w') as f:
            f.write(Review.get_csv_header_v2())
            for review in reviews:
                f.write(review.get_csv_line())
            f.close()
        self.log('Saved %s reviews to file %s' % (len(reviews), filename))

        try:
            current_time = time.time()
            average_time = (current_time - self.start_time) / int(self.scraped_pages)
            pages_left = int(review_last_page) - int(review_current_page)
            secs = pages_left * average_time
            mins = (pages_left * average_time) / 60
            hours = (pages_left * average_time) / 3600
            self.log('Reviews: %s/%s | %s seconds left | %s minutes left | %s hours left' % (
                review_current_page, review_last_page, secs, mins, hours))
        except:
            self.log('Reviews: %s/%s' % (review_current_page, review_last_page))

        if next_review_page_url is not "":
            yield self.request(next_review_page_url, self.parse)

    def retry_page(self, url):
        yield self.request(url, self.parse)
