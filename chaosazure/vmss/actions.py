import os
import random

from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import init_client
from chaosazure.rgraph.resource_graph import fetch_resources
from chaosazure.vmss.constants import RES_TYPE_VMSS
from chaosazure.machine.constants import OS_LINUX, OS_WINDOWS
from chaosazure.vmss.vmss_fetcher import fetch_vmss_instances

__all__ = ["delete_vmss", "restart_vmss", "stop_vmss", "deallocate_vmss"]


def delete_vmss(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Delete a virtual machine scale set instance at random.

    **Be aware**: Deleting a VMSS instance is an invasive action. You will not
    be able to recover the VMSS instance once you deleted it.

     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start delete_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Deleting instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.delete(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def restart_vmss(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Restart a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start restart_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Restarting instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.restart(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def stop_vmss(filter: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Stop a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start stop_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Stopping instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.power_off(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def deallocate_vmss(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Deallocate a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start deallocate_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Deallocating instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.deallocate(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def stress_vmss_instance_cpu(filter: str = None,
                             duration: int = 120,
                             timeout: int = 60,
                             configuration: Configuration = None,
                             secrets: Secrets = None):
    """
    Stress CPU up to 100% at random machines.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage.
        Defaults to 120 seconds.
    timeout : int
        Additional wait time (in seconds) for stress operation to be completed.
        Getting and sending data from/to Azure may take some time so it's not
        recommended to set this value to less than 30s. Defaults to 60 seconds.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stress_vmss_instance_cpu("where resourceGroup=='rg'", configuration=c,
                    secrets=s)
    Stress all machines from the group 'rg'

    >>> stress_vmss_instance_cpu("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Stress the machine from the group 'rg' having the name 'name'

    >>> stress_vmss_instance_cpu("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Stress two machines at random from the group 'rg'
    """

    logger.debug(
        "Start stress_cpu: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    m = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    name = m['name']
    group = vmss['resourceGroup']
    os_type = __get_os_type(m)
    if os_type == OS_WINDOWS:
        command_id = 'RunPowerShellScript'
        script_name = "cpu_stress_test.ps1"
    elif os_type == OS_LINUX:
        command_id = 'RunShellScript'
        script_name = "cpu_stress_test.sh"
    else:
        raise FailedActivity(
            "Cannot run CPU stress test on OS: %s" % os_type)

    with open(os.path.join(os.path.dirname(__file__),
                           "../scripts", script_name)) as file:
        script_content = file.read()

    parameters = {
        'command_id': command_id,
        'script': [script_content],
        'parameters': [
            {'name': "duration", 'value': duration}
        ]
    }

    logger.debug(
        "Stressing instance: {}".format(m['name']))
    client = init_client(secrets, configuration)
    poller = client.virtual_machine_scale_set_vms.run_command(
        vmss['resourceGroup'],
        vmss['name'],
        m['instanceId'],
        parameters)

    result = poller.result(duration + timeout)  # Blocking till executed
    if result:
        logger.debug(result.value[0].message)  # stdout/stderr
    else:
        raise FailedActivity(
            "stress_vmss_instance_cpu operation did not finish on time. "
            "You may consider increasing timeout setting.")


###############################################################################
# Private helper functions
###############################################################################
def choose_vmss_instance_at_random(vmss_choice, configuration, secrets):
    vmss_instances = fetch_vmss_instances(vmss_choice, configuration, secrets)
    if not vmss_instances:
        logger.warning("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")
    else:
        logger.debug(
            "Found virtual machine scale set instances: {}".format(
                [x['name'] for x in vmss_instances]))
    choice_vmss_instance = random.choice(vmss_instances)
    return choice_vmss_instance


def choose_vmss_at_random(filter, configuration, secrets):
    vmss = fetch_resources(filter, RES_TYPE_VMSS, secrets, configuration)
    if not vmss:
        logger.warning("No virtual machine scale sets found")
        raise FailedActivity("No virtual machine scale sets found")
    else:
        logger.debug(
            "Found virtual machine scale sets: {}".format(
                [x['name'] for x in vmss]))
    return random.choice(vmss)


def __get_os_type(m):
    os_type = m['osType']
    if os_type not in (OS_LINUX, OS_WINDOWS):
        raise FailedActivity("Unknown OS Type: %s" % os_type)

    return os_type
