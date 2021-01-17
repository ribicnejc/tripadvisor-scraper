import time

from masters.gecko_spiders.reviews_gecko import GeckoReviewSpider
from masters.utils.timer_utils import Timer

counter = 1
domain = "https://www.tripadvisor.com"
while counter != 0:
    start_time = time.time()
    parent_url = "/Attraction_Review-g274873-d12987385-Reviews-Avtobusna_postaja_Ljubljana-Ljubljana_Upper_Carniola_Region.html"
    site = GeckoReviewSpider(domain + parent_url)
    site.select_all_languages()
    scraped_pages = 0
    while site.has_next_review_page():  # there might be issue if there is just one review page!!!
        site.scrap_page(parent_url, scraped_pages, start_time, domain)
        scraped_pages += 1
        site.next_page()
    site.scrap_page(parent_url, scraped_pages, start_time, domain)
    site.stop_spider()
    counter -= 1
