# https://www.tripadvisor.com/Attractions-g187768-Activities-oa20-Italy.html
# https://www.tripadvisor.co.uk/Attractions-g274862-Activities-Slovenia.html
# https://www.tripadvisor.co.uk/Tourism-g274862-Slovenia-Vacations.html
# https://www.tripadvisor.co.uk/Attractions-g274862-Activities-oa20-Slovenia.html

# https://www.tripadvisor.com/Attractions-g274862-Activities-oa70-Slovenia.html#LOCATION_LIST

import scrapy
import time
import pathlib

from masters.data_structures.Province import Province
from masters.utils import unicode_utils, file_utils
from time import sleep
from os import listdir


class ProvincesSpider(scrapy.Spider):
    name = "provinces"
    root_url = 'https://www.tripadvisor.com'
    urls = []

    def __init__(self, country='', **kwargs):
        print(country)
        self.extra_data_pages = -1
        self.extra_data = False
        self.parent_url = country
        self.start_time = time.time()
        self.urls.append(country)
        self.scraped_pages = 0
        super(ProvincesSpider, self).__init__(**kwargs)

    def request(self, url, callback):
        request_with_cookies = scrapy.Request(
            url=(self.root_url + url),
            callback=callback)
        return request_with_cookies

    def request_file(self, url, callback):
        base_url = str(pathlib.Path().absolute())
        request_with_cookies = scrapy.Request(
            url=("file:///" + base_url + "/" + url),
            callback=callback)
        return request_with_cookies

    def start_requests(self):
        while self.urls.__len__() > 0:
            url = self.urls.pop()
            yield self.request(url, self.parse)

    def parse(self, response):
        self.scraped_pages = self.scraped_pages + 1
        provinces = response.css('ul.geoList li')
        provinces_obj = []
        for province in provinces:
            province_name = unicode_utils.unicode_to_string(
                province.css('a::text').extract_first())
            region_name = unicode_utils.unicode_to_string(
                province.css('span::text').extract_first())
            province_url = unicode_utils.unicode_to_string(
                province.css('a::attr(href)').extract_first())
            province_obj = Province(province_name, region_name, province_url)
            provinces_obj.append(province_obj)

        next_page = response.css('div.pgLinks a.guiArw.sprite-pageNext.pid0::attr(href)').extract_first()
        current_page = response.css('div.pgLinks span.paging.pageDisplay::text').extract_first()
        last_page = response.css('div.pgLinks a.paging.taLnk.pid0::text').extract()
        if last_page is None or len(last_page) == 0:
            last_page = None
        else:
            last_page = unicode_utils.unicode_to_string(last_page[-1])

        province_group_name = unicode_utils.unicode_to_string(
            response.css('h1.heading_name::text').extract_first()).replace("\n", "").replace(" ", "_")
        province_group_name = ''.join(
            [i if ord(i) < 128 else '' for i in province_group_name])  # Clean of non ascii chars
        try:
            current_time = time.time()
            average_time = (current_time - self.start_time) / int(self.scraped_pages)
            pages_left = int(last_page) - int(current_page)
            secs = pages_left * average_time
            mins = (pages_left * average_time) / 60
            hours = (pages_left * average_time) / 3600
            self.log('Provinces: %s/%s | %s seconds left | %s minutes left | %s hours left' % (
                current_page, last_page, secs, mins, hours))
        except:
            self.log('Provinces: %s/%s' % (current_page, last_page))

        filename = 'scraped_data/data_provinces/provinces-%s-%s.csv' % (province_group_name, current_page)
        with open(filename, 'w') as f:
            f.write(Province.get_csv_header())
            for province in provinces_obj:
                f.write(province.get_csv_line())
            f.close()
        self.log('Saved file %s' % filename)

        if next_page is not None and self.extra_data is False:
            yield self.request(next_page, self.parse)

        if next_page is None or self.extra_data is True:
            self.extra_data = True
            self.extra_data_pages += 1
            root = "scraped_data/data_extra"
            # TODO print output before data is written inside the file
            # TODO script to zip files
            # TODO script to migrate files from zip to mysql
            # TODO locations to be passed to reviews scraper
            files = listdir(root)
            files = list(filter(lambda x: province_group_name in x and "edited" not in x, files))
            if self.extra_data_pages < len(files):
                file = file_utils.fix_extra_data_files(root, files[self.extra_data_pages])
                yield self.request_file(root + "/" + file, self.parse)
