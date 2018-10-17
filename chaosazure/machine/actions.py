# -*- coding: utf-8 -*-
from typing import Any, Dict

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import auth
from chaosazure.machine.picker import pick_machine_randomly

__all__ = ["delete_machine", "poweroff_machine", "restart_machine"]


def delete_machine(configuration: Configuration = None,
                   secrets: Secrets = None) -> Dict[str, Any]:
    """
    Delete machine randomly.
    """
    logger.debug(
        'Starting delete_machine: configuration=[{}]'.format(configuration))

    with auth(secrets) as cred:
        compute_client, machine = __pick_chaos_machine(configuration, cred)

        resource_group_name = machine.id.split('/')[4].lower()
        logger.debug('Deletion chaos takes over for machine {}.{}'.format(
            resource_group_name, machine.name))
        async_restart = compute_client.virtual_machines.delete(
            resource_group_name, machine.name)
        result = async_restart.result()
        logger.debug(
            'Operation status for machine deletion: {}'.format(result.status))

        return result


def poweroff_machine(configuration: Configuration = None,
                     secrets: Secrets = None) -> Dict[str, Any]:
    """
    Power off machine randomly.
    """
    logger.debug(
        'Starting poweroff_machine: configuration=[{}]'.format(configuration))
    with auth(secrets) as cred:
        compute_client, machine = __pick_chaos_machine(configuration, cred)

        resource_group_name = machine.id.split('/')[4].lower()
        logger.debug('Powering off chaos takes over for machine {}.{}'.format(
            resource_group_name, machine.name))
        async_restart = compute_client.virtual_machines.power_off(
            resource_group_name, machine.name)
        result = async_restart.result()
        logger.debug(
            'Operation status for machine power off: {}'.format(result.status))

        return result


def restart_machine(configuration: Configuration = None,
                    secrets: Secrets = None) -> Dict[str, Any]:
    """
    Restart machine randomly.
    """
    logger.debug(
        'Starting restart_machine: configuration=[{}]'.format(configuration))
    with auth(secrets) as cred:
        compute_client, machine = __pick_chaos_machine(configuration, cred)

        resource_group_name = machine.id.split('/')[4].lower()
        logger.debug('Restarting chaos takes over for machine {}.{}'.format(
            resource_group_name, machine.name))
        async_restart = compute_client.virtual_machines.restart(
            resource_group_name, machine.name)
        result = async_restart.result()
        logger.debug(
            'Operation status for machine restart: {}'.format(result.status))

        return result


def __pick_chaos_machine(configuration, cred):
    azure_subscription_id = configuration['azure']['subscription_id']
    resource_client = ResourceManagementClient(cred, azure_subscription_id)
    compute_client = ComputeManagementClient(cred, azure_subscription_id)
    resource_groups_list = resource_client.resource_groups.list()
    machines_list_all = compute_client.virtual_machines.list_all()
    groups = configuration['azure']['resource_groups'].split(',')
    machine = pick_machine_randomly(resource_groups_list, machines_list_all,
                                    groups)
    return compute_client, machine
