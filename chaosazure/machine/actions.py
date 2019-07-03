# -*- coding: utf-8 -*-
import os
from azure.mgmt.compute import ComputeManagementClient
from chaosazure import auth
from chaosazure.machine.constants import RES_TYPE_VM, OS_LINUX, OS_WINDOWS
from chaosazure.rgraph.resource_graph import fetch_resources
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

__all__ = ["delete_machines", "stop_machines", "restart_machines",
           "start_machines", "stress_cpu", "fill_disk"]


def delete_machines(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Delete virtual machines at random.

    **Be aware**: Deleting a machine is an invasive action. You will not be
    able to recover the machine once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_machines("where resourceGroup=='rg'", c, s)
    Delete all machines from the group 'rg'

    >>> delete_machines("where resourceGroup=='rg' and name='name'", c, s)
    Delete the machine from the group 'rg' having the name 'name'

    >>> delete_machines("where resourceGroup=='rg' | sample 2", c, s)
    Delete two machines at random from the group 'rg'
    """
    logger.debug(
        "Start delete_machines: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    for m in machines:
        group = m['resourceGroup']
        name = m['name']
        logger.debug("Deleting machine: {}".format(name))
        client.virtual_machines.delete(group, name)


def stop_machines(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Stop virtual machines at random.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stop_machines("where resourceGroup=='rg'", c, s)
    Stop all machines from the group 'rg'

    >>> stop_machines("where resourceGroup=='mygroup' and name='myname'", c, s)
    Stop the machine from the group 'mygroup' having the name 'myname'

    >>> stop_machines("where resourceGroup=='mygroup' | sample 2", c, s)
    Stop two machines at random from the group 'mygroup'
    """
    logger.debug(
        "Start stop_machines: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    for m in machines:
        group = m['resourceGroup']
        name = m['name']
        logger.debug("Stopping machine: {}".format(name))
        client.virtual_machines.power_off(group, name)


def restart_machines(filter: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Restart virtual machines at random.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> restart_machines("where resourceGroup=='rg'", c, s)
    Restart all machines from the group 'rg'

    >>> restart_machines("where resourceGroup=='rg' and name='name'", c, s)
    Restart the machine from the group 'rg' having the name 'name'

    >>> restart_machines("where resourceGroup=='rg' | sample 2", c, s)
    Restart two machines at random from the group 'rg'
    """
    logger.debug(
        "Start restart_machines: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    for m in machines:
        group = m['resourceGroup']
        name = m['name']
        logger.debug("Restarting machine: {}".format(name))
        client.virtual_machines.restart(group, name)


def start_machines(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Start virtual machines at random. Thought as a rollback action.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> start_machines("where resourceGroup=='rg'", c, s)
    Start all stopped machines from the group 'rg'

    >>> start_machines("where resourceGroup=='rg' and name='name'", c, s)
    Start the stopped machine from the group 'rg' having the name 'name'

    >>> start_machines("where resourceGroup=='rg' | sample 2", c, s)
    Start two stopped machines at random from the group 'rg'
    """

    logger.debug(
        "Start start_machines: configuration='{}', filter='{}'".format(
            configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    stopped_machines = __fetch_all_stopped_machines(client, machines)
    __start_stopped_machines(client, stopped_machines)


def stress_cpu(filter: str = None,
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

    >>> stress_cpu("where resourceGroup=='rg'", configuration=c, secrets=s)
    Stress all machines from the group 'rg'

    >>> stress_cpu("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Stress the machine from the group 'rg' having the name 'name'

    >>> stress_cpu("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Stress two machines at random from the group 'rg'
    """

    logger.debug(
        "Start stress_cpu: configuration='{}', filter='{}'".format(
            configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)

    for m in machines:
        name = m['name']
        group = m['resourceGroup']
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
                               "scripts", script_name)) as file:
            script_content = file.read()

        parameters = {
            'command_id': command_id,
            'script': [script_content],
            'parameters': [
                {'name': "duration", 'value': duration}
            ]
        }

        logger.debug("Stressing CPU of machine: {}".format(name))
        poller = client.virtual_machines.run_command(group, name, parameters)
        result = poller.result(duration + timeout)  # Blocking till executed
        if result:
            logger.debug(result.value[0].message)  # stdout/stderr
        else:
            raise FailedActivity(
                "stress_cpu operation did not finish on time. "
                "You may consider increasing timeout setting.")


def fill_disk(filter: str = None,
              duration: int = 120,
              timeout: int = 60,
              size: int = 1000,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Fill the disk with random data.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Lifetime of the file created. Defaults to 120 seconds.
    timeout : int
        Additional wait time (in seconds)
        for filling operation to be completed.
        Getting and sending data from/to Azure may take some time so it's not
        recommended to set this value to less than 30s. Defaults to 60 seconds.
    size : int
        Size of the file created on the disk. Defaults to 1GB.


    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> fill_disk("where resourceGroup=='rg'", configuration=c, secrets=s)
    Fill all machines from the group 'rg'

    >>> fill_disk("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Fill the machine from the group 'rg' having the name 'name'

    >>> fill_disk("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Fill two machines at random from the group 'rg'
    """

    logger.debug(
        "Start fill_disk: configuration='{}', filter='{}'".format(
            configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)

    for m in machines:
        name = m['name']
        group = m['resourceGroup']
        os_type = __get_os_type(m)
        if os_type == OS_WINDOWS:
            command_id = 'RunPowerShellScript'
            script_name = "fill_disk.ps1"
        elif os_type == OS_LINUX:
            command_id = 'RunShellScript'
            script_name = "fill_disk.sh"
        else:
            raise FailedActivity(
                "Cannot run disk filling test on OS: %s" % os_type)

        with open(os.path.join(os.path.dirname(__file__),
                               "scripts", script_name)) as file:
            script_content = file.read()

        logger.debug("Script content: {}".format(script_content))
        parameters = {
            'command_id': command_id,
            'script': [script_content],
            'parameters': [
                {'name': "duration", 'value': duration},
                {'name': "size", 'value': size}
            ]
        }

        logger.debug("Filling disk of machine: {}".format(name))
        poller = client.virtual_machines.run_command(group, name, parameters)
        result = poller.result(duration + timeout)  # Blocking till executed
        logger.debug("Execution result: {}".format(poller))
        if result:
            logger.debug(result.value[0].message)  # stdout/stderr
        else:
            raise FailedActivity(
                "fill_disk operation did not finish on time. "
                "You may consider increasing timeout setting.")


###############################################################################
# Private helper functions
###############################################################################
def __start_stopped_machines(client, stopped_machines):
    for machine in stopped_machines:
        logger.debug("Starting machine: {}".format(machine['name']))
        client.virtual_machines.start(machine['resourceGroup'],
                                      machine['name'])


def __fetch_all_stopped_machines(client, machines) -> []:
    stopped_machines = []
    for m in machines:
        i = client.virtual_machines.instance_view(m['resourceGroup'],
                                                  m['name'])
        for s in i.statuses:
            status = s.code.lower().split('/')
            if status[0] == 'powerstate' and (
                    status[1] == 'deallocated' or status[1] == 'stopped'):
                stopped_machines.append(m)
                logger.debug("Found stopped machine: {}".format(m['name']))
    return stopped_machines


def __fetch_machines(filter, configuration, secrets) -> []:
    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    if not machines:
        logger.warning("No virtual machines found")
        raise FailedActivity("No virtual machines found")
    else:
        logger.debug(
            "Fetched virtual machines: {}".format(
                [x['name'] for x in machines]))
    return machines


def __get_os_type(machine):
    os_type = machine['properties']['storageProfile']['osDisk']['osType'] \
        .lower()
    if os_type not in (OS_LINUX, OS_WINDOWS):
        raise FailedActivity("Unknown OS Type: %s" % os_type)

    return os_type


def __compute_mgmt_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id)

        return client
