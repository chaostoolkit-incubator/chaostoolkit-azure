import io
import json
from chaoslib import Configuration, Secrets
from chaosazure.cli.graph_query import filter_type_command
from chaosazure.cli.runner import execute
from chaosazure.vmss.commands import list_vmss_instances_command
from chaosazure.vmss.constants import RES_TYPE_VMSS


def pick_vmss(filter: str,
              configuration: Configuration,
              secrets: Secrets):
    command = filter_type_command(RES_TYPE_VMSS, filter)
    result_json = __fetch_vmss_result(command, configuration, secrets)
    vmss = __parse_vmss_result(result_json)
    return vmss


def pick_vmss_instances(choice, configuration, secrets):
    command = list_vmss_instances_command(choice)
    result_json = __fetch_vmss_instances_result(command, configuration,
                                                secrets)
    vmss_instances = __parse_vmss_instances_result(result_json)
    return vmss_instances


###############################################################################
# Private helper functions
###############################################################################
def __fetch_vmss_instances_result(command, configuration, secrets):
    f = io.StringIO("")
    execute(configuration, secrets, command, f)
    result_json = json.loads(f.getvalue())
    f.close()
    return result_json


def __parse_vmss_instances_result(result_json):
    vmss_instances = []
    for elem in result_json:
        m = {
            'name': elem['name'],
            'resourceGroup': elem['resourceGroup'],
            'instanceId': elem['instanceId']
        }
        vmss_instances.append(m)
    return vmss_instances


def __fetch_vmss_result(command, configuration, secrets):
    f = io.StringIO("")
    execute(configuration, secrets, command, f)
    result_json = json.loads(f.getvalue())
    f.close()
    return result_json


def __parse_vmss_result(result_json):
    vmss = []
    for elem in result_json:
        m = {
            'name': elem['name'],
            'resourceGroup': elem['resourceGroup']
        }
        vmss.append(m)
    return vmss
