from chaoslib import Configuration, Secrets

from chaosazure.machine.constants import RES_TYPE_VM
from chaosazure.rgraph.resource_graph import fetch_resources


def fetch_machines(query: str, secrets: Secrets, configuration: Configuration):
    machines = fetch_resources(query, RES_TYPE_VM, secrets, configuration)
    results = __parse_result(machines)

    return results


###############################################################################
# Private helper functions
###############################################################################
def __parse_result(result_json):

    machines = []
    for elem in result_json:
        m = {
            'name': elem['name'],
            'resourceGroup': elem['resourceGroup']
        }
        machines.append(m)

    return machines
