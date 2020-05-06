from chaoslib.exceptions import FailedActivity, InterruptExecution
from logzero import logger

from chaosazure import init_client
from chaosazure.machine.constants import OS_LINUX, OS_WINDOWS


def prepare_path(machine: dict, path: str):
    os_type = __get_os_type(machine)
    if os_type == OS_LINUX:
        result = "/root/burn" if path is None else path
    else:
        result = "C:/burn" if path is None else path

    return result


def prepare(machine: dict, script: str):
    os_type = __get_os_type(machine)
    if os_type == OS_LINUX:
        command_id = 'RunShellScript'
        script_name = "{}.sh".format(script)
    else:
        if script == 'network_latency':
            raise InterruptExecution("Network latency is not supported "
                                     "for '{}'".format(OS_WINDOWS))
        command_id = 'RunPowerShellScript'
        script_name = ".ps1".format(script)

    return command_id, script_name


def run(resource_group: str, name: str, machine: dict,
        timeout: int, parameters: dict, secrets, configuration,
        error_msg: str = ''):
    client = init_client(secrets, configuration)
    poller = client.virtual_machine_scale_set_vms.run_command(
        resource_group,
        name,
        machine['instanceId'],
        parameters)

    result = poller.result(timeout)  # Blocking till executed
    if result and result.value:
        logger.debug(result.value[0].message)  # stdout/stderr
    else:
        raise FailedActivity("Operation did not finish properly. {}"
                             .format(error_msg))


#####################
# HELPER FUNCTIONS
####################
def __get_os_type(machine):
    os_type = machine['osType']
    if os_type not in (OS_LINUX, OS_WINDOWS):
        raise FailedActivity("Unknown OS Type: %s" % os_type)

    return os_type
