import io
import json

from chaoslib import Configuration, Secrets

from chaosazure.machine.constants import RES_TYPE_VM
from chaosazure.cli.runner import execute
from chaosazure.cli.graph_query import filter_type_command


def pick_machines(configuration: Configuration, secrets: Secrets, filter: str):
    command = filter_type_command(RES_TYPE_VM, filter)
    result_json = __fetch_result(command, configuration, secrets)
    machines = __parse_result(result_json)

    return machines


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

    machines = []
    for elem in result_json:
        m = {
            'name': elem['name'],
            'resourceGroup': elem['resourceGroup']
        }
        machines.append(m)

    return machines
