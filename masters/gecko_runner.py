from masters.gecko_spiders.reviews_gecko import GeckoReviewSpider
from masters.utils.timer_utils import Timer

counter = 1
while counter != 0:
    site = GeckoReviewSpider("https://www.tripadvisor.com/Attraction_Review-g274873-d12987385-Reviews-Avtobusna_postaja_Ljubljana-Ljubljana_Upper_Carniola_Region.html")
    site.select_all_languages()
    while site.has_next_review_page():  # there might be issue if there is just one review page!!!
        # site.scrap_page()
        site.next_page()
    site.stop_spider()
    counter -= 1
