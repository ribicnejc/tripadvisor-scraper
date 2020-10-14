class ReviewInfomap(object):
    def __init__(self, location_name,
                 location_tags,
                 lat,
                 lng,
                 review_id,
                 review_date,
                 user_id,
                 place_rate,
                 review_rate,
                 username,
                 parent_url,
                 country_of_origin,
                 attraction):
        self.review_rate = review_rate
        self.place_rate = place_rate
        self.user_id = user_id
        self.review_date = int(review_date)
        self.review_id = review_id
        self.lng = lng
        self.lat = lat
        self.location_tags = location_tags
        self.location_name = location_name
        self.username = username
        self.parent_url = parent_url
        self.country_of_origin = country_of_origin
        self.attraction = attraction
