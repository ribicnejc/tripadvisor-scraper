import scrapy

from scrapy import signals
from masters.data_structures.Attraction import Attraction
from masters.utils import unicode_utils


class LocationsSpider(scrapy.Spider):
    name = "locations"
    root_url = 'https://www.tripadvisor.com'
    current_review_coordinates = ""
    urls = [
        '/Attractions-g274862-Activities-Slovenia.html',
    ]

    def request(self, url, callback):
        request_with_cookies = scrapy.Request(
            url=(self.root_url + url),
            callback=callback)
        request_with_cookies.cookies['TALanguage'] = 'ALL'
        return request_with_cookies

    def start_requests(self):
        while self.urls.__len__() > 0:
            url = self.urls.pop()
            yield self.request(url, self.parse_first)

    def parse_first(self, response):
        attractions = response.css('div.ap_filter_wrap div.navigation_list')[-1].css(
            'div.ap_navigator a.taLnk::attr(href)')

        attractions_obj = []
        for attraction in attractions[:-1]:
            attraction_name = attraction.root.split('-')[-1].replace(".html", "")
            attraction_obj = Attraction(attraction_name, attraction.root)
            attractions_obj.append(attraction_obj)

        more_attractions = attractions[-1].root

        for attraction in attractions_obj:
            # TODO remove bellow line
            attraction.attraction_url = '/Attractions-g274873-Activities-Ljubljana_Upper_Carniola_Region.html'
            yield self.request(attraction.attraction_url, self.parse_attraction)

        """Scrap next global location"""
        yield self.request(more_attractions, self.parse_pagination)

    def parse_pagination(self, response):
        attractions = response.css('ul.geoList li a::attr(href)')
        page_num = unicode_utils.unicode_to_string(
            response.css('div.pgLinks span.pageDisplay::text').extract_first())
        next_page = response.css('div.pgLinks a.sprite-pageNext::attr(href)').extract_first()
        if next_page:
            next_page = unicode_utils.unicode_to_string(next_page)

        attractions_obj = []
        for attraction in attractions:
            attraction_name = attraction.root.split('-')[-1].replace(".html", "")
            attraction_obj = Attraction(attraction_name, attraction.root)
            attractions_obj.append(attraction_obj)

        location_group_name = response.url.replace(".html", "").split("-Activities-")[1]
        filename = 'scraped_data/data_attractions/attractions-%s-%s.csv' % (location_group_name, page_num)
        with open(filename, 'w') as f:
            for attraction in attractions_obj:
                f.write(attraction.get_csv_line())
        self.log('Saved file %s' % filename)
        yield self.request(next_page, self.parse_pagination)

    def parse_attraction(self, response):
        attraction_list = response.css('.attractions-attraction-overview-main-TopPOIs__name--GndbY').css('::attr(href)')
        attractions_obj = []
        for attraction in attraction_list:
            attraction_name = attraction.root.split('-')[-1].replace(".html", "")
            attraction_obj = Attraction(attraction_name, attraction.root)
            attractions_obj.append(attraction_obj)

        location_group_name = response.url.replace(".html", "").split("-Activities-")[1]
        next_page = response \
            .css('div.attractions-attraction-overview-main-Pagination__button--1up7M a::attr(href)') \
            .extract_first()
        # attractions-attraction-overview-main-Pagination__link--2m5mV
        # attractions-attraction-overview-main-Pagination__selected--2updu
        page_num = response.css('div.attractions-attraction-overview-main-Pagination__selected--2updu span::text')\
            .extract_fist()
        if not next_page:
            next_page = unicode_utils.unicode_to_string(next_page)
        filename = 'scraped_data/data_attractions/attractions-%s-%s.csv' % (location_group_name, 1)
        with open(filename, 'w') as f:
            for attraction in attractions_obj:
                f.write(attraction.get_csv_line())
        self.log('Saved file %s' % filename)
        yield self.request(next_page, self.parse_pagination)
