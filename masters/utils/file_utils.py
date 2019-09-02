def location_scraped(string):
    filename = 'logs/scraped_locations.log'
    with open(filename) as f:
        return string in f.read()
