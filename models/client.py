from threading import Semaphore
from time import perf_counter

CATEGORIES = ['A', 'B', 'C']

class Client:
    def __init__(self, client_id: int, client_category: str):
        self.id = client_id
        self.category = client_category
        self.semaphore = Semaphore(value=0)
        self.queue_wait = 0
        self.ticket = None

    def wait(self):
        start = perf_counter()
        self.semaphore.acquire()
        end = perf_counter()
        self.queue_wait = end - start

    def leave(self):
        self.ticket.leave_show()

    def receive_ticket(self, ticket):
        self.ticket = ticket
        self.semaphore.release()

    def info(self):
        return dict(
            id=self.id,
            category=self.category,
            wait=self.queue_wait
        )
