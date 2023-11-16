from copy import deepcopy

def parse_clients_params(params):
    clients_params = deepcopy(params)
    del clients_params['capacity']
    return clients_params

def parse_ixphere_params(params):
    ixphere_params = deepcopy(params)
    del ixphere_params['clients']
    del ixphere_params['permanence']
    del ixphere_params['max_interval']
    return ixphere_params

def parse_params(args):
    valid_args = args[1:]
    n_args = len(valid_args)
    required_params = [
        'clients',
        'capacity',
        'permanence',
        'max_interval',
        'seed',
        'time_unit'
    ]
    n_params = len(required_params)
    if n_args == n_params:
        params = [(required_params[i], int(valid_args[i])) for i in range(n_params)]
        all_params = dict(params)
        ixphere_params = parse_ixphere_params(all_params)
        clients_params = parse_clients_params(all_params)
        return ixphere_params, clients_params
    else:
        raise Exception(f"Insufficient parameters: Required [{n_params}], Given [{n_args}]")
