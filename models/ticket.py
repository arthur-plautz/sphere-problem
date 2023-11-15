from threading import Semaphore

class Ticket:
    def __init__(self, occupation):
        self.semaphore = Semaphore()
        self.occupation = occupation
