class Logger(object):
    def __init__(self, spider_name):
        self.spider_name = spider_name.lower()
        self.spider_name = self.spider_name.replace(" ", "-")

    @staticmethod
    def log_review(text):
        filename = 'logs/reviews.log'
        with open(filename, 'a+') as f:
            f.write(text + "\n")
            print(text)
            f.close()

    @staticmethod
    def log_time(text):
        filename = 'logs/timer.log'
        with open(filename, 'a+') as f:
            f.write(text + "\n")
            print(text)

    @staticmethod
    def log_location(text):
        filename = 'logs/scraped_locations.log'
        with open(filename, 'a+') as f:
            f.write(text + "\n")
            print("Added to scraped locations: " + text)
            f.close()
