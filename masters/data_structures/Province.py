class Province(object):
    # Province(obcina) URL example: https://www.tripadvisor.com/Attractions-g187768-Activities-oa20-Italy.html

    def __init__(self, province_name,
                 region_name,
                 province_url):
        self.province_name = self.clean_value(province_name)
        self.region_name = self.clean_value(region_name)
        self.province_url = self.clean_value(province_url)

    def get_csv_line(self):
        return "{}, {}, {}\n".format(
            self.province_name,
            self.region_name,
            self.province_url
        )

    @staticmethod
    def get_csv_header():
        return "province_name, " \
               "region_name, " \
               "province_url\n"

    @staticmethod
    def clean_value(value):
        return str(value).replace(",", "&&")


