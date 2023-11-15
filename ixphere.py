import sys
from models.utils import parse_params
from models.clients import Clients
from models.ixphere import Ixphere
from models.queue import Queue

if __name__ == '__main__':
    ixphere_params, clients_params = parse_params(sys.argv)
    print(f"[Ixfera] Simulacao iniciada")

    queue = Queue()
    ixphere = Ixphere(queue=queue, **ixphere_params)
    clients = Clients(queue=queue, **clients_params)

    ixphere.start()
    clients.start()
    clients.join()
    ixphere.join()

    print(f"[Ixfera] Simulacao finalizada")
