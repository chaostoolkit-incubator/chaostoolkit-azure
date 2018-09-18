# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from chaoslib.types import Configuration, Secrets

__all__ = ["describe_instances", "count_instances"]


def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


def collect_virtual_machines(compute_client, configuration, resource_client):
    virtual_machines = list()
    for resource_group in resource_client.resource_groups.list():
        if resource_group.name in configuration.group:
            for virtual_machine in compute_client.virtual_machines.list(resource_group.name):
                virtual_machines.append(virtual_machine)
    return virtual_machines


def describe_instances(filters: List[Dict[str, Any]],
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> Dict[str, Any]:
    """
    Describe Azure virtual machines.
    """
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)

    virtual_machines = collect_virtual_machines(compute_client, configuration, resource_client)

    return virtual_machines


def count_instances(filters: List[Dict[str, Any]],
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> int:
    """
    Return count of Azure virtual machines.
    """
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)

    virtual_machines = collect_virtual_machines(compute_client, configuration, resource_client)

    return len(virtual_machines)
