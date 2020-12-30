# -*- coding: utf-8 -*-

import sys
import os

from os import listdir
from scrapy import cmdline
from masters.utils.file_utils import location_scraped
from masters.utils.logger_utils import Logger

sys.path.append("..")

print("Scraper started...")

root = "scraped_data/data_provinces/ukr"
# for province in listdir(root):
#     f = open(root + "/" + province, 'r')
#     while True:
#         location = f.readline()
#         location = location.rstrip().split(", ")[2]
#         if not location:
#             break
#         if location == "province_url":
#             continue
#         if not location_scraped(location):
#             command = "scrapy crawl locations -a province=" + location
#             os.system(command)
#             Logger.log_location(location)
#         else:
#             print("Location already scraped: " + location)
cmdline.execute("scrapy crawl locations -a province=/Attractions-g2554468-Activities-Kalush_Ivano_Frankivsk_Oblast.html".split())