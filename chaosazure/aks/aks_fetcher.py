from chaoslib import Configuration, Secrets

from chaosazure.aks.constants import RES_TYPE_AKS
from chaosazure.rgraph.resource_graph import fetch_resources


def fetch_aks(query: str, secrets: Secrets, configuration: Configuration):
    aks = fetch_resources(query, RES_TYPE_AKS, secrets, configuration)
    results = __parse_result(aks)

    return results


###############################################################################
# Private helper functions
###############################################################################
def __parse_result(result_json):
    aks = []
    for elem in result_json:
        m = {
            'name': elem['name'],
            'resourceGroup': elem['resourceGroup'],
            'nodeResourceGroup': elem['properties']['nodeResourceGroup']
        }
        aks.append(m)

    return aks
