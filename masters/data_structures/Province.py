class Province(object):
    # Province(obcina) URL example: https://www.tripadvisor.com/Attractions-g187768-Activities-oa20-Italy.html

    def __init__(self, province_name,
                 province_tags,
                 parent_url):
        self.province_name = province_name
        self.province_tags = province_tags
        self.parent_url = parent_url

    def get_csv_line(self):
        return "{}, {}, {}\n".format(
            self.province_name,
            self.province_tags,
            self.parent_url
        )

    @staticmethod
    def get_csv_header():
        return "province_name, " \
               "province_tags," \
               "parent_url\n"
