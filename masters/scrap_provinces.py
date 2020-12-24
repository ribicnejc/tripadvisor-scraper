# -*- coding: utf-8 -*-
from scrapy import cmdline
import sys

sys.path.append("..")

print("Scraper started...")

cmdline.execute("scrapy crawl provinces -a country=/Attractions-g294473-Activities-oa20-Ukraine.html".split())
