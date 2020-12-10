class Review(object):
    def __init__(self,
                 review_location_name,
                 review_current_page,
                 review_last_page,
                 review_location_type,
                 review_location_breadcrumbs,
                 review_location_rate,
                 location_lat,
                 location_lng,
                 location_parent_id,
                 location_parent_name,
                 location_grandparent_id,
                 location_grandparent_name,
                 location_full_ids,
                 review_id,
                 review_date,
                 review_experience_date,
                 review_rate,
                 user_name,
                 user_link,
                 user_id,
                 parent_url
                 ):
        self.review_location_name = self.clean_value(review_location_name)
        self.review_current_page = self.clean_value(review_current_page)
        self.review_last_page = self.clean_value(review_last_page)
        self.review_location_type = self.clean_value(review_location_type)
        self.review_location_breadcrumbs = self.clean_value(review_location_breadcrumbs)
        self.review_location_rate = self.clean_value(review_location_rate)
        self.location_lat = self.clean_value(location_lat)
        self.location_lng = self.clean_value(location_lng)
        self.location_parent_id = self.clean_value(location_parent_id)
        self.location_parent_name = self.clean_value(location_parent_name)
        self.location_grandparent_id = self.clean_value(location_grandparent_id)
        self.location_grandparent_name = self.clean_value(location_grandparent_name)
        self.location_full_ids = self.clean_value(location_full_ids)
        self.review_id = self.clean_value(review_id)
        self.review_date = self.clean_value(review_date)
        self.review_experience = self.clean_value(review_experience_date)
        self.review_rate = self.clean_value(review_rate)
        self.user_name = self.clean_value(user_name)
        self.user_link = self.clean_value(user_link)
        self.user_id = self.clean_value(user_id)
        self.parent_url = self.clean_value(parent_url)

    def get_csv_line(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(
            self.review_location_name,
            self.review_current_page,
            self.review_last_page,
            self.review_location_type,
            self.review_location_breadcrumbs,
            self.review_location_rate,
            self.location_lat,
            self.location_lng,
            self.location_parent_id,
            self.location_parent_name,
            self.location_grandparent_id,
            self.location_grandparent_name,
            self.location_full_ids,
            self.review_id,
            self.review_date,
            self.review_experience,
            self.review_rate,
            self.user_name,
            self.user_link,
            self.user_id,
            self.parent_url
        )

    @staticmethod
    def clean_value(value):
        return str(value).replace(",", "&&")

    @staticmethod
    def get_csv_header_v2():
        return "review_location_name," \
               "review_current_page," \
               "review_last_page," \
               "review_location_type," \
               "review_location_breadcrumbs," \
               "review_location_rate," \
               "location_lat," \
               "location_lng," \
               "location_parent_id," \
               "location_parent_name," \
               "location_grandparent_id," \
               "location_grandparent_name," \
               "location_full_ids," \
               "review_id," \
               "review_date," \
               "review_experience_date," \
               "review_rate," \
               "user_name," \
               "user_link," \
               "user_id," \
               "parent_url\n"
