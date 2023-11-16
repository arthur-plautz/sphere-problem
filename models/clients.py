from concurrent.futures import ThreadPoolExecutor
from models.generation import RandomGeneration
from threading import Lock, Thread
from models.client import Client, CATEGORIES
from models.queue import Queue

class Clients(RandomGeneration, Thread):
    def __init__(self, queue: Queue, seed: int, time_unit: int, clients: int, permanence: int, max_interval: int):
        RandomGeneration.__init__(self, seed, time_unit)
        Thread.__init__(self)

        self.queue = queue
        self.total_clients = clients
        self.permanence = permanence
        self.max_interval = max_interval
        self._executor = ThreadPoolExecutor(max_workers=clients)

        self.data = []
        self.data_lock = Lock()

    def stats(self):
        categories = dict.fromkeys(CATEGORIES)
        for c in categories:
            categories[c] = []

        for client in self.data:
            client_category = client.get('category')
            client_wait = client.get('wait')
            categories[client_category].append(client_wait)
        
        print("\nTempo medio de espera:")
        for category, wait in categories.items():
            n = len(wait)
            w = sum(wait)/n
            print(f"Faixa {category}: {str(w)[:4]}")

    def action(self, client: Client):
        self.queue.add(client)
        print(f"[Pessoa {client.id} / {client.category}] Aguardando na fila")
        client.wait()
        
        print(f"[Pessoa {client.id} / {client.category}] Entrou na Ixfera (quantidade = {client.ticket.occupation})")
        self.generate_time(self.permanence, random=False)
        client.leave()
        print(f"[Pessoa {client.id} / {client.category}] Saiu da Ixfera (quantidade = {client.ticket.occupation})")

        with self.data_lock:
            self.data.append(client.info())

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
        self.stats()

