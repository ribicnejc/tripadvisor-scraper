# -*- coding: utf-8 -*-
from scrapy import cmdline
import sys

sys.path.append("..")

print("Scraper started...")

# https://www.tripadvisor.com/Attractions-g274873-Activities-Ljubljana_Upper_Carniola_Region.html
# https://www.tripadvisor.com/Attractions-g187881-Activities-Cagliari_Province_of_Cagliari_Sardinia.html
# cmdline.execute("scrapy crawl locations".split())
# TODO scrap location from that URL -> https://www.tripadvisor.com/Attractions-g187881-Activities-Cagliari_Province_of_Cagliari_Sardinia.html
cmdline.execute("scrapy crawl locations -a province=/Attractions-g274873-Activities-Ljubljana_Upper_Carniola_Region.html".split())