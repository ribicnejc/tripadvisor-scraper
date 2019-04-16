from queue import Queue


class Frontier(object):
    def __init__(self):
        self.frontier = Queue()
        self.already_added = set()

    def get_next(self):
        return self.frontier.get()

    def is_empty(self):
        return self.frontier.empty()

    def add_url(self, url):
        if url not in self.already_added:
            self.frontier.put(url)
            self.already_added.add(url)


frontier = Frontier()


def get_next():
    url = frontier.get_next()
    return url


def is_not_empty():
    return not (frontier.is_empty())


def add_url(url):
    frontier.add_url(url)


def plant_seeds():
    add_url("https://www.tripadvisor.com/Attractions-g274862-Activities-Slovenia.html#LOCATION_LIST")
