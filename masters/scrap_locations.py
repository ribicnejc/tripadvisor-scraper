# -*- coding: utf-8 -*-
from scrapy import cmdline
import sys

sys.path.append("..")

print("Scraper started...")

# TODO for loop for scraping locations
cmdline.execute("scrapy crawl locations -a province=/Attractions-g274873-Activities-Ljubljana_Upper_Carniola_Region.html".split())