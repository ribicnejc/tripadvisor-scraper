# -*- coding: utf-8 -*-
from scrapy import cmdline
location = "/Attraction_Review-g274873-d298666-Reviews-Ljubljana_Old_Town-Ljubljana_Upper_Carniola_Region.html"
# cmdline.execute("scrapy crawl locations".split())
cmdline.execute(("scrapy crawl reviews -a location=" + location).split())
