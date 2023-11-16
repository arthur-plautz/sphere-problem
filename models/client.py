from threading import Semaphore
from time import time_ns

CATEGORIES = ['A', 'B', 'C']

class Client:
    def __init__(self, client_id: int, client_category: str):
        self.id = client_id
        self.category = client_category
        self.semaphore = Semaphore(value=0)
        self.queue_wait = 0
        self.ticket = None

    def wait(self):
        start = time_ns()
        self.semaphore.acquire()
        end = time_ns()
        self.queue_wait = end - start

    def leave(self):
        self.ticket.semaphore.release()

    def receive_ticket(self, ticket):
        self.ticket = ticket

    def info(self):
        return dict(
            id=self.id,
            category=self.category,
            wait=self.queue_wait
        )
