class Attraction(object):
    def __init__(self, attraction_name,
                 attraction_url):
        self.attraction_url = attraction_url
        self.attraction_name = attraction_name

    def get_csv_line(self):
        return "{}\n".format(self.attraction_url)
