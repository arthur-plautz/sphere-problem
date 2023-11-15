import sys
from models.utils import parse_params
from models.clients import Clients

if __name__ == '__main__':
    ixphere_params, clients_params = parse_params(sys.argv)
    clients = Clients(**clients_params)
    clients.generate_clients()
