import time
import random

class RandomGeneration:
    def __init__(self, seed, time_unit):
        self.seed = seed
        self.time_unit = time_unit/1000
        random.seed(seed)

    def shuffle(self, array):
        random.shuffle(array)
        return array

    def generate_random(self, start=0, end=1):
        return random.randint(start, end)

    def generate_time(self, max_time):
        s = self.generate_random(end=max_time)
        time.sleep(s*self.time_unit)
