from threading import Lock, Semaphore
from models.client import Client

class Queue:
    def __init__(self):
        self.lock = Lock()
        self.semaphore = Semaphore(value=0)
        self._data = []

    @property
    def empty(self):
        with self.lock:
            return len(self._data) == 0

    def add(self, client: Client):
        with self.lock:
            self._data.append(client)
        self.semaphore.release()

    def remove(self):
        self.semaphore.acquire()
        with self.lock:
            return self._data.pop(0)

    def next(self):
        self.semaphore.acquire()
        with self.lock:
            client = self._data[0]
            self.semaphore.release()
            return client
