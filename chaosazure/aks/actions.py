import random

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.aks.picker import pick_aks
from chaosazure.machine.actions import delete_machine, poweroff_machine, \
    restart_machine

__all__ = ["delete_node", "poweroff_node", "restart_node"]


def delete_node(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Delete a node at random from a managed Azure Kubernetes Service.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start delete_node: configuration='{}', filter='{}'".format(
            configuration, filter))

    filter_nodes = __filter_node_resource_group(filter, configuration, secrets)
    delete_machine(configuration, secrets, filter_nodes)


def poweroff_node(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Power off a node at random from a managed Azure Kubernetes Service.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start poweroff_node: configuration='{}', filter='{}'".format(
            configuration, filter))

    filter_nodes = __filter_node_resource_group(filter, configuration, secrets)
    poweroff_machine(configuration, secrets, filter_nodes)


def restart_node(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Restart a node at random from a managed Azure Kubernetes Service.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start restart_node: configuration='{}', filter='{}'".format(
            configuration, filter))

    filter_nodes = __filter_node_resource_group(filter, configuration, secrets)
    restart_machine(configuration, secrets, filter_nodes)


def __filter_node_resource_group(filter, configuration, secrets):
    aks = pick_aks(configuration, secrets, filter)
    logger.debug("Found AKS clusters: {}".format([x['name'] for x in aks]))
    choice_aks = random.choice(aks)
    node_resource_group = choice_aks['nodeResourceGroup']
    filter_nodes = "where resourceGroup =~ '{}'".format(node_resource_group)
    return filter_nodes
