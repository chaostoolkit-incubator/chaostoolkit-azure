import random

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.aks.aks_fetcher import fetch_aks
from chaosazure.machine.actions import delete_machine, stop_machine, \
    restart_machine

__all__ = ["delete_node", "stop_node", "restart_node"]


def delete_node(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Delete a node at random from a managed Azure Kubernetes Service.

    **Be aware**: Deleting a node is an invasive action. You will not be able
    to recover the node once you deleted it.

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

    query = __create_query_for_aks_node(filter, configuration, secrets)
    delete_machine(query, configuration, secrets)


def stop_node(filter: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Stop a node at random from a managed Azure Kubernetes Service.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start stop_node: configuration='{}', filter='{}'".format(
            configuration, filter))

    query = __create_query_for_aks_node(filter, configuration, secrets)
    stop_machine(query, configuration, secrets)


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

    query = __create_query_for_aks_node(filter, configuration, secrets)
    restart_machine(query, configuration, secrets)


###############################################################################
# Private helper functions
###############################################################################
def __create_query_for_aks_node(query, configuration, secrets):
    fetched_aks = fetch_aks(query, secrets, configuration)
    logger.debug(
        "Found AKS clusters: {}".format([x['name'] for x in fetched_aks]))
    aks = random.choice(fetched_aks)
    node_resource_group = aks['nodeResourceGroup']
    query_nodes = "where resourceGroup =~ '{}'".format(node_resource_group)
    return query_nodes
