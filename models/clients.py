from concurrent.futures import ThreadPoolExecutor
from models.generation import RandomGeneration
from threading import Lock, Thread
from models.client import Client, CATEGORIES
from models.queue import Queue
from time import time_ns

class Clients(RandomGeneration, Thread):
    def __init__(self, queue: Queue, seed: int, time_unit: int, clients: int, max_interval: int):
        RandomGeneration.__init__(self, seed, time_unit)
        Thread.__init__(self)

        self.queue = queue
        self.total_clients = clients
        self.max_interval = max_interval
        self._executor = ThreadPoolExecutor(max_workers=clients)

        self.data = []
        self.data_lock = Lock()

    def action(self, client: Client):
        self.queue.add(client)
        print(f"[Pessoa {client.id} / {client.category}] Aguardando na fila")

        start = time_ns()
        client.semaphore.acquire()
        end = time_ns()
        print(f"[Pessoa {client.id} / {client.category}] Entrou na Ixfera (quantidade = {client.ticket.occupation})")
        client.ticket.semaphore.acquire()
        print(f"[Pessoa {client.id} / {client.category}] Saiu da Ixfera (quantidade = {client.ticket.occupation})")

        total_wait = end - start
        client.update_waiting(total_wait)

        with self.data_lock:
            self.data.append(client.to_dict())

    def new_client(self, client_id: int, client_category: str):
        self.generate_time(self.max_interval)
        client = Client(client_id, client_category)
        self._executor.submit(self.action, client)

    def generate_categories(self):
        n_categories = len(CATEGORIES)
        client_categories = [CATEGORIES[i % n_categories] for i in range(self.total_clients)]
        return self.shuffle(client_categories)

    def run(self):
        categories = self.generate_categories()
        for i in range(self.total_clients):
            self.new_client(i, categories[i])
        self._executor.shutdown()
