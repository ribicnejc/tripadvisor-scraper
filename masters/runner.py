# -*- coding: utf-8 -*-
import os

from scrapy import cmdline
from os import listdir
from masters.utils.logger_utils import Logger
from masters.utils.file_utils import location_scraped

# cmdline.execute("scrapy crawl locations".split())
root = "scraped_data/data_attractions/"
for attraction in listdir(root):
    f = open(root + attraction, 'r')
    while True:
        location = f.readline()
        location = location.rstrip()
        if not location:
            break
        if not location_scraped(location):
            os.system("scrapy crawl reviews -a location=" + location)
        Logger.log_location(location)
