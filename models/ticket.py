from threading import Semaphore

class Ticket:
    def __init__(self, occupation):
        self.semaphore = Semaphore(value=0)
        self.occupation = occupation

    def leave_show(self):
        self.semaphore.release()

    def end_show(self):
        self.semaphore.acquire()
