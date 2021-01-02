from zipfile import ZipFile
from os import listdir

locations = "locations_ukr.zip"
provinces = "provinces_ukr.zip"
reviews = "reviews_ukr.zip"

with ZipFile(provinces, 'w') as zipProvinces:
    root = "../scraped_data/data_provinces/ukr"
    files = listdir(root)
    print("Zipping provinces...")
    for file in files:
        zipProvinces.write(root + "/" + file)
    print("Provinces zipped.")

with ZipFile(locations, 'w') as zipLocations:
    root = "../scraped_data/data_locations/ukr"
    files = listdir(root)
    print("Zipping locations...")
    for file in files:
        zipLocations.write(root + "/" + file)
    print("Locations zipped.")

with ZipFile(reviews, 'w') as zipReviews:
    root = "../scraped_data/data_reviews/ukr"
    files = listdir(root)
    print("Zipping reviews...")
    for file in files:
        zipReviews.write(root + "/" + file)
    print("Reviews zipped.")
