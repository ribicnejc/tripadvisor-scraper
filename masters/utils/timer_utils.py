import time


class Timer(object):

    def __init__(self):
        self.start_execution = 0
        self.stop_execution = 0

    def reset_timer(self):
        self.start_execution = 0
        self.stop_execution = 0

    def start_timer(self):
        self.start_execution = time.time()

    def stop_timer(self):
        self.stop_execution = time.time()
        self.print_time()

    def print_time(self):
        return "Time of execution: %s" % (self.stop_execution - self.start_execution)
