# -*- coding: utf-8 -*-
import random

from azure.mgmt.compute import ComputeManagementClient
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import auth
from chaosazure.machine.constants import RES_TYPE_VM
from chaosazure.rgraph.resource_graph import fetch_resources

__all__ = ["delete_machine", "stop_machine", "restart_machine"]


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

    choice = choose_machine_at_random(filter, configuration, secrets)

    logger.debug("Deleting machine: {}".format(choice['name']))
    client = init_client(secrets, configuration)
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

    choice = choose_machine_at_random(filter, configuration, secrets)

    logger.debug("Stopping machine: {}".format(choice['name']))
    client = init_client(secrets, configuration)
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

    choice = choose_machine_at_random(filter, configuration, secrets)

    logger.debug("Restarting machine: {}".format(choice['name']))
    client = init_client(secrets, configuration)
    client.virtual_machines.restart(choice['resourceGroup'], choice['name'])


###############################################################################
# Private helper functions
###############################################################################
def choose_machine_at_random(filter, configuration, secrets):
    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    if not machines:
        logger.warning("No virtual machines found")
        raise FailedActivity("No virtual machines found")
    else:
        logger.debug(
            "Found virtual machines: {}".format(
                [x['name'] for x in machines]))
    choice = random.choice(machines)
    return choice


def init_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id)

        return client
