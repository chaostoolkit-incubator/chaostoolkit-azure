import os

from chaoslib.exceptions import FailedActivity, InterruptExecution
from logzero import logger

from chaosazure import init_client
from chaosazure.machine.constants import OS_LINUX, OS_WINDOWS, RES_TYPE_VM
from chaosazure.vmss.constants import RES_TYPE_VMSS_VM

UNSUPPORTED_WINDOWS_SCRIPTS = ['network_latency', 'burn_io']


def prepare_path(machine: dict, path: str):
    os_type = __get_os_type(machine)
    if os_type == OS_LINUX:
        result = "/root/burn" if path is None else path
    else:
        result = "C:/burn" if path is None else path

    return result


def prepare(machine: dict, script: str):
    _os_type = __get_os_type(machine)
    if _os_type == OS_LINUX:
        _command_id = 'RunShellScript'
        _script_name = "{}.sh".format(script)
    else:
        if script in UNSUPPORTED_WINDOWS_SCRIPTS:
            raise InterruptExecution("'{}' is not supported for os '{}'"
                                     .format(script, OS_WINDOWS))
        _command_id = 'RunPowerShellScript'
        _script_name = "{}.ps1".format(script)

    _file_path = os.path.join(
        os.path.dirname(__file__), "../scripts", _script_name)
    with open(_file_path) as _file_path:
        _script_content = _file_path.read()
        return _command_id, _script_content


def run(machine: dict, timeout: int, parameters: dict,
        secrets, configuration):
    client = init_client(secrets, configuration)

    machine_type = machine.get('type').lower()
    if machine_type == RES_TYPE_VMSS_VM.lower():
        poller = client.virtual_machine_scale_set_vms.run_command(
            machine['resourceGroup'], machine['name'],
            machine['instanceId'], parameters)

    elif machine_type == RES_TYPE_VM.lower():
        poller = client.virtual_machines.run_command(
            machine['resourceGroup'], machine['name'], parameters)

    else:
        msg = "Trying to run a command for the unknown resource type '{}'" \
            .format(machine.get('type'))
        raise InterruptExecution(msg)

    result = poller.result(timeout)  # Blocking till executed
    if result and result.value:
        logger.debug(result.value[0].message)  # stdout/stderr
    else:
        raise FailedActivity("Operation did not finish properly."
                             " You may consider increasing timeout setting.")


#####################
# HELPER FUNCTIONS
####################
def __get_os_type(machine):
    machine_type = machine['type'].lower()

    if machine_type == RES_TYPE_VMSS_VM.lower():
        os_type = machine['osType']

    elif machine_type == RES_TYPE_VM.lower():
        os_type = machine['properties']['storageProfile']['osDisk']['osType']

    else:
        msg = "Trying to run a command for the unknown resource type '{}'" \
            .format(machine.get('type'))
        raise InterruptExecution(msg)

    if os_type.lower() not in (OS_LINUX, OS_WINDOWS):
        raise FailedActivity("Unknown OS Type: %s" % os_type)

    return os_type.lower()
