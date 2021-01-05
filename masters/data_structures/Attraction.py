class Attraction(object):
    def __init__(self, attraction_name, attraction_rate, attraction_type, attraction_url, attraction_parent_url):
        self.attraction_url = self.clean_value(attraction_url)
        self.attraction_name = self.clean_value(attraction_name)
        self.attraction_type = self.clean_value(attraction_type)
        self.attraction_rate = self.clean_value(attraction_rate)
        self.attraction_parent_url = self.clean_value(attraction_parent_url)

    def get_csv_line(self):
        return "{}, {}, {}, {}, {}\n".format(
            self.attraction_name,
            self.attraction_rate,
            self.attraction_type,
            self.attraction_url,
            self.attraction_parent_url)

    @staticmethod
    def clean_value(value):
        return str(value).replace(",", "&&").replace("\"", "'")

    @staticmethod
    def get_csv_header():
        return "attraction_name, " \
               "attraction_rate, " \
               "attraction_type, " \
               "attraction_url, " \
               "attraction_parent_url\n"
