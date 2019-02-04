# -*- coding: utf-8 -*-
import os
import random

from azure.mgmt.compute import ComputeManagementClient
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import auth
from chaosazure.machine.constants import RES_TYPE_VM, OS_LINUX, OS_WINDOWS
from chaosazure.rgraph.resource_graph import fetch_resources

__all__ = ["delete_machine", "stop_machine", "restart_machine",
           "start_machine", "stress_cpu"]


def delete_machine(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Delete a virtual machines at random.

    ***Be aware**: Deleting a machine is an invasive action. You will not be
    able to recover the machine once you deleted it.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start delete_machine: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_machine_at_random(filter, configuration, secrets)

    logger.debug("Deleting machine: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.virtual_machines.delete(choice['resourceGroup'], choice['name'])


def stop_machine(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Stop a virtual machines at random.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start stop_machine: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_machine_at_random(filter, configuration, secrets)

    logger.debug("Stopping machine: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.virtual_machines.power_off(choice['resourceGroup'], choice['name'])


def restart_machine(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Restart a virtual machines at random.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start restart_machine: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_machine_at_random(filter, configuration, secrets)

    logger.debug("Restarting machine: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.virtual_machines.restart(choice['resourceGroup'], choice['name'])


def start_machine(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Start a virtual machine that is in a stopped state.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all stopped
        machines in the subscription will be started again.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """

    logger.debug(
        "Start start_machine: configuration='{}', filter='{}'".format(
            configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __init_client(secrets, configuration)
    stopped_machines = __fetch_stopped_machines(client, machines)
    __start_stopped_machines(client, stopped_machines)


def stress_cpu(filter: str = None,
               duration: int = 120,
               timeout: int = 60,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """
    Stress CPU up to 100% at random machine.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    duration : int
        Duration of the stress test (in seconds) that generates high CPU usage
    timeout : int
        Additional wait time (in seconds) for stress operation to be completed.
        Getting and sending data from/to Azure may take some time so it's not
        recommended to set this value to lower than 30s
    """
    logger.debug(
        "Start stress_cpu: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_machine_at_random(filter, configuration, secrets)

    logger.debug("Stressing CPUs machine: {}".format(choice['name']))
    client = __init_client(secrets, configuration)

    os_type = __get_os_type(choice)
    if os_type == OS_WINDOWS:
        command_id = 'RunPowerShellScript'
        script_name = "cpu_stress_test.ps1"
    elif os_type == OS_LINUX:
        command_id = 'RunShellScript'
        script_name = "cpu_stress_test.sh"
    else:
        raise FailedActivity("Cannot run CPU stress test on OS: %s" % os_type)

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

    poller = client.virtual_machines.run_command(
        choice['resourceGroup'], choice['name'], parameters)
    result = poller.result(duration + timeout)  # Blocking till executed
    if result:
        logger.debug(result.value[0].message)  # stdout/stderr
    else:
        raise FailedActivity("stress_cpu operation did not finish on time. "
                             "You may consider increasing timeout setting.")


###############################################################################
# Private helper functions
###############################################################################
def __start_stopped_machines(client, stopped_machines):
    for machine in stopped_machines:
        logger.debug("Starting machine: {}".format(machine['name']))
        client.virtual_machines.start(machine['resourceGroup'],
                                      machine['name'])


def __fetch_stopped_machines(client, machines):
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


def __fetch_machines(filter, configuration, secrets):
    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    if not machines:
        logger.warning("No virtual machines found")
        raise FailedActivity("No virtual machines found")
    else:
        logger.debug(
            "Fetched virtual machines: {}".format(
                [x['name'] for x in machines]))
    return machines


def __fetch_machine_at_random(filter, configuration, secrets):
    machines = __fetch_machines(
        filter, configuration=configuration, secrets=secrets)
    choice = random.choice(machines)
    return choice


def __get_os_type(machine):
    os_type = machine['properties']['storageProfile']['osDisk']['osType']\
        .lower()
    if os_type not in (OS_LINUX, OS_WINDOWS):
        raise FailedActivity("Unknown OS Type: %s" % os_type)

    return os_type


def __init_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id)

        return client
