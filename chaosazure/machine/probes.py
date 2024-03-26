# -*- coding: utf-8 -*-
import logging

from chaoslib.types import Configuration, Secrets

from chaosazure.machine.constants import RES_TYPE_VM
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_machines", "count_machines"]
logger = logging.getLogger("chaostoolkit")


def describe_machines(
    filter: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
):
    """
    Describe Azure virtual machines.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start describe_machines: configuration='{}', filter='{}'".format(
            configuration, filter
        )
    )

    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    return machines


def count_machines(
    filter: str = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> int:
    """
    Return count of Azure virtual machines.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start count_machines: configuration='{}', filter='{}'".format(
            configuration, filter
        )
    )

    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    return len(machines)
