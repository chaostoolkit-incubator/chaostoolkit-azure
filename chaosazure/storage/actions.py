# -*- coding: utf-8 -*-
import re
import random

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_storage_management_client
from chaosazure.common import cleanse
from chaosazure.storage.constants import RES_TYPE_SRV_SA
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["delete_storage_accounts", "delete_blob_containers"]

from chaosazure.vmss.records import Records


def delete_storage_accounts(filter: str = None,
                            configuration: Configuration = None,
                            secrets: Secrets = None):
    """
    Delete storage accounts at random.

    **Be aware**: Deleting a storage account is a invasive action. You will not be
    able to recover the storage account once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the storage accounts. If the filter is omitted all storage accounts in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_storage_accounts("where resourceGroup=='rg'", c, s)
    Delete all storage accounts from the group 'rg'

    >>> delete_storage_accounts("where resourceGroup=='rg' and name='name'", c, s)
    Delete the storage accounts from the group 'rg' having the name 'name'

    >>> delete_storage_accounts("where resourceGroup=='rg' | sample 2", c, s)
    Delete two storage accounts at random from the group 'rg'
    """
    logger.debug(
        "Start delete_storage_accounts: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    storage_accounts = __fetch_storage_accounts(filter, configuration, secrets)

    client = __storage_mgmt_client(secrets, configuration)
    storage_accounts_records = Records()

    for sa in storage_accounts:
        group = sa['resourceGroup']
        name = sa['name']
        client.storage_accounts.delete(group, name)
        storage_accounts_records.add(cleanse.storage_account(sa))

    return storage_accounts_records.output_as_dict('resources')


def delete_blob_containers(filter: str = None,
                           name_pattern: str = None,
                           number: int = None,
                           configuration: Configuration = None,
                           secrets: Secrets = None):
    """
    Delete blob containers at random.

    **Be aware**: Deleting a blob container is a invasive action. You will not be
    able to recover the blob container once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the storage account. If the filter is omitted all storage accounts in
        the subscription will have their blob containers selected as potential chaos candidates.
    name_pattern : str, optional
        Filter the blob containers. If the filter is omitted all blob containers will be selected
        for the probe.
        Pattern example:
        'container[0-9]{3}'
    number : int, optional
        Pick the number of blob containers matching the two filters that will be deleted. If the
        number is omitted all blob containers in the list will be deleted.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_blob_containers("where resourceGroup=='rg'", c, s)
    Delete all blob containers from the group 'rg'

    >>> delete_blob_containers("where resourceGroup=='rg' and name='name'", c, s)
    Delete the blob containers from the group 'rg' under the storage account named 'name'

    >>> delete_blob_containers("where resourceGroup=='rg'", "chaos-*", c, s)
    Delete the blob containers from the group 'rg' matching the "chaos-*" pattern

    >>> delete_blob_containers("where resourceGroup=='rg'", "chaos-*", 3, c, s)
    Delete 3 blob containers at random from the group 'rg' matching the "chaos-*" pattern
    """
    logger.debug(
        "Start delete_blob_containers: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    if number == 0:
        raise FailedActivity("Cannot target 0 volumes")

    pattern = None
    if name_pattern:
        pattern = re.compile(name_pattern)

    storage_accounts = __fetch_storage_accounts(filter, configuration, secrets)

    client = __storage_mgmt_client(secrets, configuration)
    blob_storage_records = Records()

    containers_to_target = []

    for sa in storage_accounts:
        group = sa['resourceGroup']
        name = sa['name']
        containers = client.blob_containers.list(group, name)
        for container in containers:
            if pattern is None or pattern.search(container.name):
                containers_to_target.append({"group": group, "storage_name": name,
                                             "container_name": container.name})

    if not containers_to_target:
        raise FailedActivity("No blob containers to target found")

    if not number or number > len(containers_to_target):
        containers_to_delete = containers_to_target
    else:
        containers_to_delete = random.sample(containers_to_target, number)

    for container in containers_to_delete:
        logger.debug("Deleting container: {}/{}".format(container['storage_name'],
                     container['container_name']))
        client.blob_containers.delete(container['group'], container['storage_name'],
                                      container['container_name'])
        blob_storage_records.add(container)
    return blob_storage_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################


def __fetch_storage_accounts(filter, configuration, secrets) -> []:
    logger.debug(RES_TYPE_SRV_SA)
    storage_accounts = fetch_resources(filter, RES_TYPE_SRV_SA, secrets, configuration)
    logger.debug(storage_accounts)
    if not storage_accounts:
        logger.warning("No Storage accounts found")
        raise FailedActivity("No Storage accounts found")
    else:
        logger.debug("Fetched storage accounts: {}".format(
                     [n['name'] for n in storage_accounts]))
    return storage_accounts


def __storage_mgmt_client(secrets, configuration):
    return init_storage_management_client(secrets, configuration)
