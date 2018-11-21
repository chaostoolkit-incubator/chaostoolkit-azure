import io
import json

from chaoslib import Configuration, Secrets

from chaosazure.aks.constants import RES_TYPE_AKS
from chaosazure.cli.graph_query import filter_type_command
from chaosazure.cli.runner import execute


def pick_aks(configuration: Configuration, secrets: Secrets, filter: str):
    command = filter_type_command(RES_TYPE_AKS, filter)
    result_json = __fetch_result(command, configuration, secrets)
    aks = __parse_result(result_json)

    return aks


###############################################################################
# Private helper functions
###############################################################################
def __fetch_result(command, configuration, secrets):

    f = io.StringIO("")
    execute(configuration, secrets, command, f)
    result_json = json.loads(f.getvalue())
    f.close()

    return result_json


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
