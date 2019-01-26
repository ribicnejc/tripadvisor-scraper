from masters.spiders_sel.reviews_sel import SeleniumReviewSpider

site = SeleniumReviewSpider(
    "https://www.tripadvisor.com/Attraction_Review-g644300-d7289577-Reviews-Tourist_Information_Centre_Kranj_House-Kranj_Upper_Carniola_Region.html")

# site.select_all_languages()
while site.has_next_review_page():
    site.scrap_page()
    site.next_page()

site.stop_spider()
