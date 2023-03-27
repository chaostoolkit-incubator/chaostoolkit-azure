# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.netapp.constants import RES_TYPE_SRV_NV
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_netapp_volumes", "count_netapp_volumes"]


def describe_netapp_volumes(filter: str = None,
                            configuration: Configuration = None,
                            secrets: Secrets = None):
    """
    Describe Azure netapp volumes.

    Parameters
    ----------
    filter : str
        Filter the netapp volumes. If the filter is omitted all netapp volumes in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start describe_netapp_volumes: configuration='{}', filter='{}'".format(
            configuration, filter))

    netapp_volumes = fetch_resources(filter, RES_TYPE_SRV_NV, secrets, configuration)
    return netapp_volumes


def count_netapp_volumes(filter: str = None,
                         configuration: Configuration = None,
                         secrets: Secrets = None) -> int:
    """
    Return count of Azure netapp volumes.

    Parameters
    ----------
    filter : str
        Filter the netapp volumes. If the filter is omitted all netapp_volumes in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start count_netapp_volumes: configuration='{}', filter='{}'".format(
            configuration, filter))

    netapp_volumes = fetch_resources(filter, RES_TYPE_SRV_NV, secrets, configuration)
    return len(netapp_volumes)
