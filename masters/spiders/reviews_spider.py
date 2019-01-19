import scrapy
import unicodedata

from masters.spiders_sel import reviews_sel


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    root_url = 'https://www.tripadvisor.com'
    current_review_coordinates = ""
    urls = [
        '/Attraction_Review-g644300-d7289577-Reviews-Tourist_Information_Centre_Kranj_House-Kranj_Upper_Carniola_Region.html',
    ]

    def start_requests(self):
        for url in self.urls:
            self.current_review_coordinates = reviews_sel.get_url(self.root_url + url)
            yield scrapy.Request(url=(self.root_url + url), callback=self.parse)

    def parse(self, response):
        next_review_page_url = self.unicode_to_string(
            response.css('div.ui_pagination a.next::attr(href)').extract_first())
        # self.urls.append(next_review_page_url)

        for review in response.css('div.review-container'):
            review_id = self.unicode_to_string(review.css('::attr(data-reviewid)').extract_first())
            user_id = self.unicode_to_string(
                review.css('div.member_info div.memberOverlayLink::attr(id)').extract_first())
            print(review)
            print(self.current_review_coordinates)

        page = response.url.split("/")[-2]
        filename = 'reviews-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def unicode_to_string(self, value):
        return unicodedata.normalize('NFKD', value).encode('utf8', 'ignore')
