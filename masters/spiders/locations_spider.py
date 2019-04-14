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

        location_group_name = response.url.replace(".html", "").split("-Activities-")[1]
        filename = 'scraped_data/data_attractions/attractions-%s-%s.csv' % (location_group_name, 1)
        with open(filename, 'w') as f:
            for attraction in attractions_obj:
                f.write(attraction.get_csv_line())
        self.log('Saved file %s' % filename)

        yield self.request(more_attractions, self.parse_pagination)

    def parse_pagination(self, response):
        attractions = response.css('div.navigation_list div.ap_navigator')

        page_num = 2 #todo get page num

