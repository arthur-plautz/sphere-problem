from concurrent.futures import ThreadPoolExecutor
from models.generation import RandomGeneration
from models.utils import tprint

class Clients(RandomGeneration):
    def __init__(self, seed, time_unit, clients, max_interval):
        super().__init__(seed, time_unit)
        self.total_clients = clients
        self.max_interval = max_interval
        self._executor = ThreadPoolExecutor(max_workers=clients)

    def new_client(self, client_id, client_category):
        self.generate_time(self.max_interval)
        client_info = (client_id, client_category)
        self._executor.submit(self.action, client_info)

    def action(self, client_info):
        client_id, client_category = client_info
        tprint(f"New Client {client_id} / {client_category}")
        for i in range(2):
            self.generate_time(self.max_interval)
            tprint(f"Client {client_id} messing around #{i}")

    def generate_categories(self):
        categories = [i%3 for i in range(self.total_clients)]
        return self.shuffle(categories)

    def generate_clients(self):
        categories = self.generate_categories()
        for i in range(self.total_clients):
            self.new_client(i, categories[i])
        self._executor.shutdown()
