import random

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.aks.constants import RES_TYPE_AKS
from chaosazure.machine.actions import delete_machines, stop_machines, \
    restart_machines
from chaosazure.rgraph.resource_graph import fetch_resources

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

    query = node_resource_group_query(filter, configuration, secrets)
    delete_machines(query, configuration, secrets)


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

    query = node_resource_group_query(filter, configuration, secrets)
    stop_machines(query, configuration, secrets)


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

    query = node_resource_group_query(filter, configuration, secrets)
    restart_machines(query, configuration, secrets)


###############################################################################
# Private helper functions
###############################################################################
def node_resource_group_query(query, configuration, secrets):
    aks = fetch_resources(query, RES_TYPE_AKS, secrets, configuration)
    if not aks:
        logger.warning("No AKS clusters found")
        raise FailedActivity("No AKS clusters found")
    else:
        logger.debug(
            "Found AKS clusters: {}".format(
                [x['name'] for x in aks]))
    choice = random.choice(aks)
    node_resource_group = choice['properties']['nodeResourceGroup']
    return "where resourceGroup =~ '{}'".format(node_resource_group)
