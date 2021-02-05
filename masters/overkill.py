# -*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append("..")
import masters
from scrapy import cmdline
from masters.utils.logger_utils import Logger
from masters.utils.file_utils import location_scraped, location_overkill, location_overkill_scraped

locations = []
f = open("logs/to_scrap.log", "r")
for x in f:
    if x not in locations:
        locations.append(x.replace("\n", ""))
f.close()

f = open("logs/scraped_overkill.log", "r")
scraped_num = -1
while True:
    location = f.readline()
    scraped_num += 1
    if not location:
        f.close()
        break

amount_of_locations = len(locations)
pages_left = amount_of_locations - scraped_num
start_time = time.time()
scraped_in_this_run = 0

for location in locations:
    location_url = location
    is_scraped = location_overkill_scraped(location_url)
    if not location_url or location_url == "attraction_url" or is_scraped:
        if location_scraped:
            print("Location already scraped: " + location_url)
            continue

    time_stamp = time.time()
    if scraped_in_this_run == 0:
        average_time = 0
    else:
        average_time = (time.time() - start_time) / scraped_in_this_run
    seconds_left = (pages_left - scraped_in_this_run) * average_time
    secs = seconds_left
    mins = seconds_left / 60
    hours = seconds_left / 3600
    Logger.log_it('Locations: %s/%s | %s seconds left | %s minutes left | %s hours left' % (
        (scraped_num + scraped_in_this_run), amount_of_locations, secs, mins, hours))

    # os.system("scrapy crawl reviews -a location=" + location_url)
    status = 0  # os.system("python3 gecko_runner.py " + location_url)
    if status == 0:
        Logger.log_overkill_location(location_url)
    scraped_in_this_run += 1
    # pages_left -= 1
