# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.common.resources.graph import fetch_resources
from chaosazure.vmss.constants import RES_TYPE_VMSS

__all__ = ["count_instances"]


def count_instances(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> int:
    """
    Return count of VMSS instances.

    Parameters
    ----------
    filter : str
        Filter the VMSS instance. If the filter is omitted all machines in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Starting count_instances: configuration='{}', filter='{}'".format(
            configuration, filter))

    instances = fetch_resources(filter, RES_TYPE_VMSS, secrets, configuration)
    return len(instances)
