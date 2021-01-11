# -*- coding: utf-8 -*-
import os
import sys
import time

from scrapy import cmdline
from masters.utils.logger_utils import Logger
from masters.utils.file_utils import location_scraped
from masters.data_managers.utils import database_utils

sys.path.append("..")

print("Scraper started...")
# location_url = "/Attraction_Review-g7060164-d9756222-Reviews-Tri_Karasya_Fishing_and_Recreation_Complex-Bilyayivka_Odessa_Oblast.html"
# location_url = "/Attraction_Review-g295368-d554746-Reviews-Odessa_National_Academic_Opera_and_Ballet_Theater-Odessa_Odessa_Oblast.html"
# location_url = "/Attraction_Review-g8480324-d21212631-Reviews-Obrt_Eva-Plitvicka_Jezera_Plitvice_Lakes_National_Park_Central_Croatia.html"
# cmdline.execute(("scrapy crawl reviews -a location=" + location_url).split())

# exit(0)

connection = database_utils.create_connection("data/databases/data.db")
locations = database_utils.get_location_urls(connection)

f = open("logs/scraped_locations.log", "r")
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
    location_url = location[7]
    is_scraped = location_scraped(location_url)
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
    secs = pages_left * average_time
    mins = (pages_left * average_time) / 60
    hours = (pages_left * average_time) / 3600
    print('Locations: %s/%s | %s seconds left | %s minutes left | %s hours left' % (
        (scraped_num + scraped_in_this_run), amount_of_locations, secs, mins, hours))

    os.system("scrapy crawl reviews -a location=" + location_url)
    Logger.log_location(location_url)
    scraped_in_this_run += 1
    #pages_left -= 1
