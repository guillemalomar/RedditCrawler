from time import time


class Timer:
    def __init__(self):
        self.start_time = time()

    def finish(self):
        print "Total time:", time() - self.start_time