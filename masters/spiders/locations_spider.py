import scrapy
import time
import re
import json

from masters.data_structures.Attraction import Attraction
from masters.utils import unicode_utils
from masters import settings


class LocationsSpider(scrapy.Spider):
    name = "locations"
    root_url = 'https://www.tripadvisor.co.uk'
    urls = []

    def __init__(self, province='', **kwargs):
        self.parent_url = province
        self.start_time = time.time()
        self.urls.append(province)
        self.scraped_pages = 0
        super(LocationsSpider, self).__init__(**kwargs)

    def request(self, url, callback):
        request_with_cookies = scrapy.Request(
            url=(self.root_url + url),
            callback=callback)
        return request_with_cookies

    def start_requests(self):
        while self.urls.__len__() > 0:
            url = self.urls.pop()
            yield self.request(url, self.parse)

    def parse(self, response):
        self.scraped_pages = self.scraped_pages + 1
        attractions_obj = []
        attractions = response.css('div._2j03JUe9.MmIH_ltD._2JdZspdU')

        if attractions is None or len(attractions) == 0:
            attractions = response.css('div.k8UcErpq div._20eVZLwe')

        for attraction in attractions:
            # Parsing attraction name
            try:
                attraction_name = unicode_utils.unicode_to_string(
                    attraction.css('div._1fqdhjoD h3').extract_first()).split("<!-- -->")[1].replace("</h3>", "")
            except:
                try:
                    attraction_name = unicode_utils.unicode_to_string(
                        attraction.css('a._3W3bcspL h3').extract_first()).split("<!-- -->")[1].replace("</h3>", "")
                except:
                    attraction_name = None

            # Parsing attraction type
            attraction_type = unicode_utils.unicode_to_string(
                attraction.css('span._21qUqkJx::text').extract_first())

            # Parsing attraction rate
            try:
                attraction_rate = unicode_utils.unicode_to_string(
                    attraction.css('svg._3KcXyP0F::attr(title)').extract_first()).split(" ")[0]
            except:
                attraction_rate = "None"

            # Parsing attraction url
            attraction_url = unicode_utils.unicode_to_string(
                attraction.css('a._255i5rcQ::attr(href)').extract_first())
            if attraction_url is None:
                attraction_url = unicode_utils.unicode_to_string(
                    attraction.css('a._3W3bcspL::attr(href)').extract_first())

            attraction_obj = Attraction(attraction_name, attraction_rate, attraction_type, attraction_url,
                                        self.parent_url)
            attractions_obj.append(attraction_obj)

        if attractions is None or len(attractions) == 0:
            attractions = response.css('div._25PvF8uO._2X44Y8hm')
            for attraction in attractions:
                attraction_name = unicode_utils.unicode_to_string(
                    attraction.css('div._6sUF3jUd a h2::text').extract_first())
                attraction_type = unicode_utils.unicode_to_string(
                    attraction.css('div._1pEzc5jw span._21qUqkJx::text').extract_first())
                try:
                    attraction_rate = unicode_utils.unicode_to_string(
                        attraction.css('div._2-JBovPw svg::attr(title)').extract_first()).split(" ")[0]
                except:
                    attraction_rate = "None"
                attraction_url = unicode_utils.unicode_to_string(
                    attraction.css('div._6sUF3jUd a._1QKQOve4::attr(href)').extract_first())
                attraction_obj = Attraction(attraction_name, attraction_rate, attraction_type, attraction_url,
                                            self.parent_url)
                attractions_obj.append(attraction_obj)

        location_group_name = response.url.replace(".html", "").split("-Activities-")[1]
        # next_page = pagination['nextLink']['url']
        next_page = unicode_utils.unicode_to_string(
            response.css('div._1r6YXRQy a._1JOGv2rJ._1qMtXLO6._3yBiBka1::attr(href)').extract_first())

        # current_page = pagination['currentPage']
        current_page = unicode_utils.unicode_to_string(
            response.css('div._1r6YXRQy span._7Rpjvz_k::text').extract_first())
        if current_page is None:
            current_page = unicode_utils.unicode_to_string(
                response.css('div.pageNumbers span.pageNum.current::text').extract_first())

        last_page = response.css('div._1r6YXRQy span._17Cv7cBt a::text').extract()
        if last_page is None or len(last_page) == 0:
            try:
                last_page = unicode_utils.unicode_to_string(
                    response.css('div.pageNumbers a.pageNum::text').extract()[-1])
                if int(last_page) <= int(current_page):
                    next_page = None
            except:
                if current_page is not None:
                    current_url = response.url.replace(self.root_url, "")
                    print("Retrying(1) " + current_url)
                    yield self.request(current_url, self.parse)
                    return

        elif last_page is not None and len(last_page) > 0:
            last_page = last_page[-1]

        try:
            last_page = int(last_page)
            current_page = int(current_page)
        except:
            self.log("Fail to convert pages: %s %s" % (last_page, current_page))

        if next_page is None and current_page is not None and current_page < last_page:
            next_page = self.parent_url.split("-Activities-")
            pagination = int(current_page) * 30
            next_page = next_page[0] + "-Activities-" + "oa" + str(pagination) + "-" + next_page[1]
            if current_page == last_page:
                next_page = None

        filename = 'scraped_data/data_locations/%s/locations-%s-%s.csv' % (
            settings.COUNTRY, location_group_name, current_page)
        with open(filename, 'w') as f:
            f.write(Attraction.get_csv_header())
            for attraction in attractions_obj:
                f.write(attraction.get_csv_line())
            f.close()
        self.log('Saved %s locations in file %s' % (len(attractions_obj), filename))

        try:
            current_time = time.time()
            average_time = (current_time - self.start_time) / int(self.scraped_pages)
            pages_left = int(last_page) - int(current_page)
            secs = pages_left * average_time
            mins = (pages_left * average_time) / 60
            hours = (pages_left * average_time) / 3600
            self.log('Locations: %s/%s | %s seconds left | %s minutes left | %s hours left' % (
                current_page, last_page, secs, mins, hours))
        except:
            self.log('Locations: %s/%s' % (current_page, last_page))

        if next_page is not None:
            yield self.request(next_page, self.parse)

        # pattern = re.compile(r'(?<=pageManifest:)(.*)(?=}\;\(this\.)')
        # pattern = re.compile(r'(?<=JSON\.parse\(\")(.*)(?=\"\)\)\);)')
        # (?<=JSON\.parse\(\")(.*)(?=\.)
        # class=\\"{0}\\">
        # tripadvisor_data = response.css('html').re(pattern)[0]
        # tripadvisor_data = tripadvisor_data.replace('\\"', "\"")

        # class=\\"{0}\\">
        # tripadvisor_data = json.loads(tripadvisor_data)
        # tmp = tripadvisor_data['urqlCache']['921471245']['data']['attractionResponse']
        # tripadvisor_data = tripadvisor_data['redux']['api']['responses']

        # location_data_key = list(filter((lambda x: '/attraction_overview/' in x), list(tripadvisor_data)))[0]
        # attractions = tripadvisor_data[location_data_key]['data']['topPOIs']['pois']
        # pagination = tripadvisor_data[location_data_key]['data']['topPOIs']['paginationModel']
