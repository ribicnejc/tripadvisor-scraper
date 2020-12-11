#https://www.tripadvisor.com/Attractions-g187768-Activities-oa20-Italy.html
#https://www.tripadvisor.co.uk/Attractions-g274862-Activities-Slovenia.html
#https://www.tripadvisor.co.uk/Tourism-g274862-Slovenia-Vacations.html
#https://www.tripadvisor.co.uk/Attractions-g274862-Activities-oa20-Slovenia.html

import scrapy

from masters.data_structures.Attraction import Attraction
from masters.utils import unicode_utils
from time import sleep


class LocationsSpider(scrapy.Spider):
    name = "locations"
    root_url = 'https://www.tripadvisor.com'
    current_review_coordinates = ""
    urls = [
        '/Attractions-g187768-Activities-Italy.html',
        '/Attractions-g187768-Activities-oa20-Italy.html'
    ]

    def request(self, url, callback):
        request_with_cookies = scrapy.Request(
            url=(self.root_url + url),
            callback=callback)
        return request_with_cookies

    def start_requests(self):
        while self.urls.__len__() > 0:
            url = self.urls.pop()
            yield self.request(url, self.parse_global_attraction)

    def parse_global_attraction(self, response):
        attractions = response.css('ul.geoList li a::attr(href)')
        if len(attractions) == 0:
            attractions = response.css('div.ap_filter_wrap div.navigation_list')[-1].css(
                'div.ap_navigator a.taLnk::attr(href)')
            more_attractions = attractions[-1].root
            attractions = attractions[:-1]  # last element is more button on first parsing
        else:
            more_attractions = response.css('div.pgLinks a.sprite-pageNext::attr(href)').extract_first()
            if more_attractions:
                more_attractions = unicode_utils.unicode_to_string(more_attractions)

        attractions_obj = []
        for attraction in attractions:
            attraction_name = attraction.root.split('-')[-1].replace(".html", "")
            attraction_obj = Attraction(attraction_name, attraction.root)
            attractions_obj.append(attraction_obj)

        """Scrap region attractions"""
        for attraction in attractions_obj:
            sleep(1)
            print("Attraction: ", attraction.attraction_url)
            yield self.request(attraction.attraction_url, self.parse_local_attraction)

        """Scrap next page of regions"""
        if more_attractions:
            yield self.request(unicode_utils.byte_to_string(more_attractions), self.parse_global_attraction)

