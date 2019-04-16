from masters.gecko_spiders.reviews_gecko import GeckoReviewSpider
from masters.utils.timer_utils import Timer

counter = 5
while counter != 0:
    site = GeckoReviewSpider("/Attractions-g12312169-Activities-Zbilje_Upper_Carniola_Region.html")
    site.select_all_languages()
    while site.has_next_review_page():  # there might be issue if there is just one review page!!!
        if not site.is_all_languages_selected():
            site.select_all_languages()
        site.scrap_page()
        site.next_page()

    site.stop_spider()
    counter -= 1
