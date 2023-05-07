import time


class MultimeterBase:
    timestamp_start = None
    timestamp_previous = None

    def __init__(self):
        self.timestamp_start = self.timestamp_previous = time.time_ns()
        self.timestamp_previous = self.timestamp_start
