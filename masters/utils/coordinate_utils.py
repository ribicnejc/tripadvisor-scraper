from masters.utils import unicode_utils


def parse_google_maps_link(link):
    coordinates = link.split("&center=")[1].split("&maptype")[0].split(",")
    return unicode_utils.unicode_to_string(coordinates[0]), unicode_utils.unicode_to_string(coordinates[1])


def parse_google_maps_link_selenium(link):
    coordinates = link.split("&center=")[1].split("&maptype")[0].split(",")
    return coordinates[0], coordinates[1]
