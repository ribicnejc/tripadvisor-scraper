class Location(object):
    def __init__(self, location_name,
                 location_url):
        self.location_url = location_url
        self.location_name = location_name

    def get_csv_line(self):
        return "{}\n".format(self.location_url)
