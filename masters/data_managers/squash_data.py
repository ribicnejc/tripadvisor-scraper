# TODO zip scraped data

from zipfile import ZipFile
from os import listdir

locations = "locations.zip"
provinces = "provinces.zip"
reviews = "reviews.zip"

with ZipFile(provinces, 'w') as zipProvinces:
    root = "../scraped_data/data_provinces"
    files = listdir(root)
    for file in files:
        zipProvinces.write(root + "/" + file)
