# -*- coding: utf-8 -*-

import sys
import os
import time

from os import listdir
from scrapy import cmdline
from masters.utils.file_utils import location_scraped
from masters.utils.logger_utils import Logger
from masters import settings

sys.path.append("..")

print("Scraper started...")

root = "scraped_data/data_provinces/" + settings.COUNTRY

# Get numbers of locations to scrap
ulrs = 0
for province in listdir(root):
    f = open(root + "/" + province, "r")
    while True:
        location = f.readline()
        ulrs += 1
        if not location:
            f.close()
            break
f = open("logs/scraped_locations.log", "r")
scraped_num = 0
while True:
    location = f.readline()
    scraped_num += 1
    if not location:
        f.close()
        break

avg_time = 3
seconds_left = (ulrs - scraped_num) * avg_time
time_stamp = time.time()
for province in listdir(root):
    f = open(root + "/" + province, 'r')
    while True:
        location = f.readline()
        scraped_num += 1
        print("Line: " + location)
        if not location:
            break
        location = location.rstrip().split(", ")[2]
        if location == "province_url":
            continue
        if not location_scraped(location):
            time_stamp = time.time()
            Logger.log_time("######### Time left: seconds %s | minutes %s | hours %s" % (
                seconds_left, seconds_left / 60, seconds_left / 60 / 60))

            command = "scrapy crawl locations -a province=" + location
            os.system(command)

            avg_time = time.time() - time_stamp
            seconds_left = (ulrs - scraped_num) * avg_time
            Logger.log_location(location)
        else:
            print("Location already scraped: " + location)

# cmdline.execute("scrapy crawl locations -a province=/Attractions-g274873-Activities-Ljubljana_Upper_Carniola_Region.html".split())
# cmdline.execute("scrapy crawl locations -a province=/Attractions-g1816350-Activities-Yaremche_Ivano_Frankivsk_Oblast.html".split())
