from masters.spiders_sel.reviews_sel import SeleniumReviewSpider
from masters.utils.timer_utils import Timer

counter = 5
while counter != 0:
    site = SeleniumReviewSpider(
        "https://www.tripadvisor.com/Attraction_Review-g644300-d7289577-Reviews-Tourist_Information_Centre_Kranj_House-Kranj_Upper_Carniola_Region.html")
    site.select_all_languages()
    while site.has_next_review_page(): #there might be issue if there is just one review page!!!
        if not site.is_all_languages_selected():
            site.select_all_languages()
        site.scrap_page()
        site.next_page()

    site.stop_spider()
    counter -= 1
