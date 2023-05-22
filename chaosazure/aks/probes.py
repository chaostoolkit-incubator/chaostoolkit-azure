# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.aks.constants import RES_TYPE_AKS
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_managed_clusters", "count_managed_clusters"]


def describe_managed_clusters(filter: str = None,
                              configuration: Configuration = None,
                              secrets: Secrets = None):
    """
    Describe Azure managed cluster.

    Parameters
    ----------
    filter : str
        Filter the managed cluster. If the filter is omitted all managed cluster in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start describe_managed_clusters: configuration='{}', filter='{}'".format(
            configuration, filter))

    managed_clusters = fetch_resources(filter, RES_TYPE_AKS, secrets, configuration)
    return managed_clusters


def count_managed_clusters(filter: str = None,
                           configuration: Configuration = None,
                           secrets: Secrets = None) -> int:
    """
    Return count of Azure managed cluster.

    Parameters
    ----------
    filter : str
        Filter the managed cluster. If the filter is omitted all managed_clusters in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start count_managed_clusters: configuration='{}', filter='{}'".format(
            configuration, filter))

    managed_clusters = fetch_resources(filter, RES_TYPE_AKS, secrets, configuration)
    return len(managed_clusters)
