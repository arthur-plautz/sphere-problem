from threading import Semaphore

CATEGORIES = ['A', 'B', 'C']

class Client:
    def __init__(self, client_id: int, client_category: str):
        self.id = client_id
        self.category = client_category
        self.semaphore = Semaphore()
        self.queue_wait = 0
        self.ticket = None

    def update_waiting(self, total_time):
        self.queue_wait = total_time

    def give_ticket(self, ticket):
        self.ticket = ticket

    def to_dict(self):
        return dict(
            id=self.id,
            category=self.category,
            wait=self.queue_wait
        )
