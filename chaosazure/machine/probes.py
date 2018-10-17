# -*- coding: utf-8 -*-

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from chaoslib.types import Configuration, Secrets

from chaosazure import auth
from chaosazure.machine.picker import pick_machines

__all__ = ["describe_machines", "count_machines"]


def describe_machines(configuration: Configuration = None,
                      secrets: Secrets = None):
    """
    Describe Azure machines.
    """
    with auth(secrets) as cred:
        machines = pick_subscribed_machines(configuration, cred)
        return machines


def count_machines(configuration: Configuration = None,
                   secrets: Secrets = None) -> int:
    """
    Return count of Azure machines.
    """
    with auth(secrets) as cred:
        machines = pick_subscribed_machines(configuration, cred)
        return len(machines)


def pick_subscribed_machines(configuration, cred):
    azure_subscription_id = configuration['azure']['subscription_id']
    resource_client = ResourceManagementClient(cred, azure_subscription_id)
    compute_client = ComputeManagementClient(cred, azure_subscription_id)
    resource_groups_list = resource_client.resource_groups.list()
    machines_list_all = compute_client.virtual_machines.list_all()
    rg = configuration['azure']['resource_groups'].split(',')
    machines = pick_machines(resource_groups_list, machines_list_all, rg)
    return machines
