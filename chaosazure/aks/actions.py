import random

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_containerservice_management_client
from chaosazure.aks.constants import RES_TYPE_AKS
from chaosazure.common import cleanse
from chaosazure.machine.actions import delete_machines, stop_machines, \
    restart_machines
from chaosazure.common.resources.graph import fetch_resources
from chaosazure.vmss.records import Records

__all__ = ["delete_node", "stop_node", "restart_node", "start_managed_clusters",
           "delete_managed_clusters", "stop_managed_clusters"]


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
    return delete_machines(query, configuration, secrets)


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
    return stop_machines(query, configuration, secrets)


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
    return restart_machines(query, configuration, secrets)


def stop_managed_clusters(filter: str = None,
                          configuration: Configuration = None,
                          secrets: Secrets = None):
    """
    Stop managed cluster at random.

    Parameters
    ----------
    filter : str, optional
        Filter the managed cluster. If the filter is omitted all managed cluster in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stop_managed_cluster("where resourceGroup=='rg'", c, s)
    Stop all managed clusters from the group 'rg'

    >>> stop_managed_cluster("where resourceGroup=='rg' and name='name'", c, s)
    Stop the managed cluster from the group 'rg' having the name 'name'

    >>> stop_managed_cluster("where resourceGroup=='rg' | sample 2", c, s)
    Stop two managed clusters at random from the group 'rg'
    """
    logger.debug(
        "Start stop_managed_cluster: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    managed_clusters = __fetch_managed_clusters(filter, configuration, secrets)
    client = __containerservice_mgmt_client(secrets, configuration)
    managed_clusters_records = Records()
    for c in managed_clusters:
        group = c['resourceGroup']
        name = c['name']
        logger.debug("Stopping managed cluster: {}".format(name))
        logger.debug(c)
        client.managed_clusters.begin_stop(group, name)
        managed_clusters_records.add(cleanse.managed_cluster(c))

    return managed_clusters_records.output_as_dict('resources')


def start_managed_clusters(filter: str = None,
                           configuration: Configuration = None,
                           secrets: Secrets = None):
    """
    Start managed cluster at random.

    Parameters
    ----------
    filter : str, optional
        Filter the managed cluster. If the filter is omitted all managed cluster in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> start_managed_cluster("where resourceGroup=='rg'", c, s)
    Stop all managed clusters from the group 'rg'

    >>> start_managed_cluster("where resourceGroup=='rg' and name='name'", c, s)
    Stop the managed cluster from the group 'rg' having the name 'name'

    >>> start_managed_cluster("where resourceGroup=='rg' | sample 2", c, s)
    Stop two managed clusters at random from the group 'rg'
    """
    logger.debug(
        "Start start_cluster: configuration='{}', filter='{}'".format(
            configuration, filter))

    managed_clusters = __fetch_managed_clusters(filter, configuration, secrets)
    client = __containerservice_mgmt_client(secrets, configuration)
    managed_clusters_records = Records()
    for c in managed_clusters:
        group = c['resourceGroup']
        name = c['name']
        logger.debug("Starting managed cluster: {}".format(name))
        client.managed_clusters.begin_start(group, name)
        managed_clusters_records.add(cleanse.managed_cluster(c))

    return managed_clusters_records.output_as_dict('resources')


def delete_managed_clusters(filter: str = None,
                            configuration: Configuration = None,
                            secrets: Secrets = None):
    """
    Delete a managed cluster at random from a managed Azure Kubernetes Service.

    **Be aware**: Deleting a managed cluster is an invasive action. You will not be
    able to recover the managed cluster once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the managed cluster. If the filter is omitted all managed cluster in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_managed_cluster("where resourceGroup=='rg'", c, s)
    Stop all managed clusters from the group 'rg'

    >>> delete_managed_cluster("where resourceGroup=='rg' and name='name'", c, s)
    Stop the managed cluster from the group 'rg' having the name 'name'

    >>> delete_managed_cluster("where resourceGroup=='rg' | sample 2", c, s)
    Stop two managed clusters at random from the group 'rg'
    """
    logger.debug(
        "Start delete_managed_cluster: configuration='{}', filter='{}'".format(
            configuration, filter))

    managed_clusters = __fetch_managed_clusters(filter, configuration, secrets)
    client = __containerservice_mgmt_client(secrets, configuration)
    managed_clusters_records = Records()
    for c in managed_clusters:
        group = c['resourceGroup']
        name = c['name']
        logger.debug("Deleting managed cluster: {}".format(name))
        client.managed_clusters.begin_delete(group, name)
        managed_clusters_records.add(cleanse.managed_cluster(c))

    return managed_clusters_records.output_as_dict('resources')


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


def __fetch_managed_clusters(filter, configuration, secrets) -> []:
    clusters = fetch_resources(filter, RES_TYPE_AKS, secrets, configuration)
    if not clusters:
        logger.warning("No Managed Clusters found")
        raise FailedActivity("No Managed Clusters found")
    else:
        logger.debug(
            "Fetched managed clusters: {}".format(
                [c['name'] for c in clusters]))
    return clusters


def __containerservice_mgmt_client(secrets, configuration):
    return init_containerservice_management_client(secrets, configuration)
