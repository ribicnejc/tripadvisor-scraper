import time
import sys

sys.path.append("..")
import masters
from masters.gecko_spiders.reviews_gecko import GeckoReviewSpider

domain = "https://www.tripadvisor.com"
start_time = time.time()
parent_url = sys.argv[1]
site = GeckoReviewSpider(domain + parent_url)
site.select_all_languages()
scraped_pages = 0

if site.is_other_page():
    site.stop_spider()
    exit(0)
#if site.is_not_ram_capable(parent_url):
#    site.stop_spider()
#    exit(1)
while site.has_next_review_page():
    site.scrap_page(parent_url, scraped_pages, start_time, domain)
    scraped_pages += 1
    site.next_page()
site.scrap_page(parent_url, scraped_pages, start_time, domain)
site.stop_spider()

