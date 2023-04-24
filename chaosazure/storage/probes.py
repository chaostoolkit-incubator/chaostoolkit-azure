# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.storage.constants import RES_TYPE_SRV_SA
from chaosazure.common.resources.graph import fetch_resources
from chaosazure.storage.actions import __storage_mgmt_client

__all__ = ["describe_storage_accounts", "count_storage_accounts", "count_blob_containers"]


def describe_storage_accounts(filter: str = None,
                              configuration: Configuration = None,
                              secrets: Secrets = None):
    """
    Describe Azure storage account.

    Parameters
    ----------
    filter : str
        Filter the storage account. If the filter is omitted all storage account in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start describe_storage_accounts: configuration='{}', filter='{}'".format(
                 configuration, filter))

    storage_accounts = fetch_resources(filter, RES_TYPE_SRV_SA, secrets, configuration)
    return storage_accounts


def count_storage_accounts(filter: str = None,
                           configuration: Configuration = None,
                           secrets: Secrets = None) -> int:
    """
    Return count of Azure storage account.

    Parameters
    ----------
    filter : str
        Filter the storage account. If the filter is omitted all storage_accounts in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start count_storage_accounts: configuration='{}', filter='{}'".format(
                 configuration, filter))

    storage_accounts = fetch_resources(filter, RES_TYPE_SRV_SA, secrets, configuration)
    return len(storage_accounts)


def count_blob_containers(filter: str = None,
                          configuration: Configuration = None,
                          secrets: Secrets = None) -> int:
    """
    Return count of Azure Blob Containers in filtered Storage account.

    Parameters
    ----------
    filter : str
        Filter the storage account. If the filter is omitted all blob containers in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start count_storage_accounts: configuration='{}', filter='{}'".format(
                 configuration, filter))

    storage_accounts = fetch_resources(filter, RES_TYPE_SRV_SA, secrets, configuration)
    client = __storage_mgmt_client(secrets, configuration)
    count = 0

    for sa in storage_accounts:
        group = sa['resourceGroup']
        name = sa['name']
        containers = client.blob_containers.list(group, name)
        count += sum(1 for _ in containers)

    return count
