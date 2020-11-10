# -*- coding: utf-8 -*-
import os
import sys

sys.path.append("..")

from scrapy import cmdline
from os import listdir
from masters.utils.logger_utils import Logger
from masters.utils.file_utils import location_scraped

print("Scraper started...")

# cmdline.execute("scrapy crawl locations".split())
#
# exit(47

# https://www.tripadvisor.com/Attraction_Review-g60763-d105127-Reviews-Central_Park-New_York_City_New_York.html

cmdline.execute("scrapy crawl reviews -a location=/Attraction_Review-g60763-d105127-Reviews-Central_Park-New_York_City_New_York.html".split())

# cmdline.execute("scrapy crawl reviews -a location=/Attraction_Review-g1887526-d11849033-Reviews-OLIMPIJCI_IZ_CRNE_NA_KOROSKEM_Olympians_from_Crna_na_Koroskem-Crna_na_Koroskem_.html".split())

root = "scraped_data/data_attractions/"
# for attraction in listdir(root):
#     f = open(root + attraction, 'r')
#     while True:
#         location = f.readline()
#         location = location.rstrip()
#         if not location:
#             break
#         if not location_scraped(location):
#             os.system("scrapy crawl reviews -a location=" + location)
#             Logger.log_location(location)
#         else:
#             print("location already scraped: " + location)

# os.system("scrapy crawl reviews -a location=/Attraction_Review-g1077241-d8587496-Reviews-Pivovarna_Lasko-Lasko_Styria_Region.html")
