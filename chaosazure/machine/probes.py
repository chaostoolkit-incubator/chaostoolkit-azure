# -*- coding: utf-8 -*-

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from chaoslib.types import Configuration, Secrets

from chaosazure import credentials
from chaosazure.machine.picker import pick_machines

__all__ = ["describe_machines", "count_machines"]


def describe_machines(configuration: Configuration = None, secrets: Secrets = None):
    """
    Describe Azure machines.
    """
    #
    # init azure clients
    #
    cred = credentials.create_from(secrets)
    resource_client = ResourceManagementClient(cred, configuration['subscription_id'])
    compute_client = ComputeManagementClient(cred, configuration['subscription_id'])

    #
    # get azure resources
    #
    resource_groups_list = resource_client.resource_groups.list()
    machines_list_all = compute_client.virtual_machines.list_all()

    #
    # pick 'em
    #
    machines = pick_machines(resource_groups_list, machines_list_all, configuration)

    return machines


def count_machines(configuration: Configuration = None,
                   secrets: Secrets = None) -> int:
    """
    Return count of Azure machines.
    """
    #
    # init azure clients
    #
    cred = credentials.create_from(secrets)
    resource_client = ResourceManagementClient(cred, configuration['subscription_id'])
    compute_client = ComputeManagementClient(cred, configuration['subscription_id'])

    #
    # get azure resources
    #
    resource_groups_list = resource_client.resource_groups.list()
    machines_list_all = compute_client.virtual_machines.list_all()

    #
    # pick 'em
    #
    machines = pick_machines(resource_groups_list, machines_list_all, configuration)

    return len(machines)
