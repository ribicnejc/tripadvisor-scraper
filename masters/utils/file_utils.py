from os import listdir
from masters.utils import unicode_utils

import functools


def location_scraped(string):
    filename = 'logs/scraped_locations.log'
    with open(filename) as f:
        return string in f.read()


def get_last_scraped_page_url(review_location_name, url):
    # https://www.tripadvisor.com/Attraction_Review-g60763-d105127-Reviews-or74990-Central_Park-New_York_City_New_York.html#REVIEWS
    # https://www.tripadvisor.com/Attraction_Review-g60763-d105127-Reviews-Central_Park-New_York_City_New_York.html#REVIEWS
    root = "scraped_data/data_reviews/"
    files = listdir(root)
    filtered_list = list(filter(lambda x: (review_location_name in x) and ("None" not in x), files))
    if len(filtered_list) == 0:
        return None
    last_file = functools.reduce(lambda a, b: sort_files(a, b, review_location_name), filtered_list)
    last_file = last_file.replace("reviews-", "") \
        .replace(review_location_name, "") \
        .replace("-", "") \
        .replace(".csv", "")
    page_number = int(last_file)
    if page_number > 1:
        page_number -= 1
    tmp = url.split("-Reviews-")
    or_name = "-or" + str((page_number * 5)) + "-"
    return tmp[0] + "-Reviews-" + or_name + tmp[1]


def sort_files(a, b, name):
    # 'reviews-Central_Park-179.csv'
    tmp_a = a.replace("reviews-", "").replace(name, "").replace("-", "").replace(".csv", "")
    tmp_b = b.replace("reviews-", "").replace(name, "").replace("-", "").replace(".csv", "")
    if int(tmp_a) > int(tmp_b):
        return a
    return b


def fix_extra_data_files(root, file):
    with open(root + "/" + file, 'r') as f:
        data = f.read()
        data = data.replace("3D", "").replace("=\r\n", "")
        new_file = file.replace(".mhtml", "")
        new_file = new_file + "_edited.mhtml"
        with open(root + "/" + new_file) as f2:
            f2.write(data)
            f2.close()
            return new_file

    # TODO remove 3D string from file
    # TODO remove "=\r\n" from file
# TODO script where you read data and clean all the garbage
