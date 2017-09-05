from time import time


class Timer:
    def __init__(self):
        """
        Init method to initalize timer and save initializing current time
        """
        self.start_time = time()

    def finish(self):
        """
        Method to stop timer and return time from start to end
        :return:
        """
        return time() - self.start_time
