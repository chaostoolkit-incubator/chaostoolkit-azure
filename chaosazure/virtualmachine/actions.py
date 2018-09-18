# -*- coding: utf-8 -*-
from typing import Any, Dict

from logzero import logger
import random

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from chaoslib.types import Configuration, Secrets

from chaosazure.types import ChaosParameters

__all__ = ["delete_instance", "poweroff_instance", "restart_instance"]


def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


def select_chaos_candidates(compute_client, configuration, resource_client):
    chaos_candidates = list()
    for resource_group in resource_client.resource_groups.list():
        if resource_group.name in configuration.group:
            for virtual_machine in compute_client.virtual_machines.list(resource_group.name):
                chaos_candidates.append((resource_group.name, virtual_machine.name))
    return chaos_candidates


def delete_instance(parameters: ChaosParameters, timeout: int = 60,
                configuration: Configuration = None,
                secrets: Secrets = None) -> Dict[str, Any]:
    """
    Delete instance randomly in your resource group.
    """
    logger.debug('Starting delete_instance: parameters=[{}], timeout=[{}], configuration=[{}]'
                 .format(parameters, timeout, configuration))
    #
    # Create all clients with an application (service principal) token provider
    #
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)

    #
    # Select candidate
    #
    chaos_candidates = select_chaos_candidates(compute_client, configuration, resource_client)
    chaos_candidate = random.choice(chaos_candidates)

    #
    # Delete instance
    #
    logger.debug('Starting \'delete chaos\' for VM: {}:{}'.format(chaos_candidate[1], chaos_candidate[0]))
    async_delete = compute_client.virtual_machines.delete(chaos_candidate[0], chaos_candidate[1])
    result = async_delete.result()
    logger.debug('Operation status for delete_instance: {}'.format(result.status))

    return result


def poweroff_instance(timeout: int = 60, configuration: Configuration = None,
               secrets: Secrets = None) -> Dict[str, Any]:
    """
    Stop instance randomly in your resource group.
    """
    logger.debug('Starting poweroff_instance: timeout=[{}], configuration=[{}]'.format(timeout, configuration))
    #
    # Create all clients with an application (service principal) token provider
    #
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)

    #
    # Select candidate
    #
    chaos_candidates = select_chaos_candidates(compute_client, configuration, resource_client)
    chaos_candidate = random.choice(chaos_candidates)

    #
    # Poweroff instance
    #
    logger.debug('Starting \'poweroff chaos\' for VM: {}:{}'.format(chaos_candidate[1], chaos_candidate[0]))
    async_poweroff = compute_client.virtual_machines.power_off(chaos_candidate[0], chaos_candidate[1])
    result = async_poweroff.result()
    logger.debug('Operation status for poweroff_instance: {}'.format(result.status))

    return result


def restart_instance(timeout: int = 60, configuration: Configuration = None,
               secrets: Secrets = None) -> Dict[str, Any]:
    """
    Restart instance randomly in your resource group.
    """
    logger.debug('Starting restart_instance: timeout=[{}], configuration=[{}]'.format(timeout, configuration))
    #
    # Create all clients with an application (service principal) token provider
    #
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)

    #
    # Select candidate
    #
    chaos_candidates = select_chaos_candidates(compute_client, configuration, resource_client)
    chaos_candidate = random.choice(chaos_candidates)

    #
    # Restart instance
    #
    logger.debug('Starting \'restart chaos\' for VM: {}:{}'.format(chaos_candidate[1], chaos_candidate[0]))
    async_restart = compute_client.virtual_machines.restart(chaos_candidate[0], chaos_candidate[1])
    result = async_restart.result()
    logger.debug('Operation status for restart_instance: {}'.format(result.status))

    return result
