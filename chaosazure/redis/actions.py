# -*- coding: utf-8 -*-
import re

from azure.mgmt.redis import RedisManagementClient
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_redis_client
from chaosazure.common import cleanse
from chaosazure.redis.constants import RES_TYPE_SRV_CACHE_REDIS
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["reboot_redis"]

from chaosazure.vmss.records import Records


def reboot_redis(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    reboot_redis redis

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    """
    logger.debug(
        "Start stop_redis: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    servers = __fetch_redis(filter, configuration, secrets)
    client = __redis__mgmt_client(secrets, configuration)
    redis_records = Records()
    for s in servers:
        group = s['resourceGroup']
        name = s['name']
        logger.debug("Deleting server: {}".format(name))
        client.redis.force_reboot(group, name)

        redis_records.add(cleanse.redis(s))

    return redis_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################
def __fetch_redis(filter, configuration, secrets) -> []:
    servers = fetch_resources(filter, RES_TYPE_SRV_CACHE_REDIS, secrets, configuration)
    if not servers:
        logger.warning("No redis found")
        raise FailedActivity("No redis found")
    else:
        logger.debug(
            "Fetched redis: {}".format(
                [s['name'] for s in servers]))
    return servers


def __redis__mgmt_client(secrets, configuration):
    return init_redis_client(secrets, configuration)
