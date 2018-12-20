# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.machine.machine_fetcher import fetch_machines

__all__ = ["describe_machines", "count_machines"]


def describe_machines(configuration: Configuration = None,
                      secrets: Secrets = None, filter: str = None):
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
            configuration, filter))

    machines = fetch_machines(configuration, secrets, filter)
    return machines


def count_machines(configuration: Configuration = None,
                   secrets: Secrets = None, filter: str = None) -> int:
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
            configuration, filter))

    machines = fetch_machines(configuration, secrets, filter)
    return len(machines)
