# -*- coding: utf-8 -*-
import re

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.redis.constants import RES_TYPE_SRV_CACHE_REDIS
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_redis"]


def describe_redis(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Describe Azure Cache for Redis.

    Parameters
    ----------
    filter : str
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start describe_servers: configuration='{}', filter='{}'".format(
            configuration, filter))

    servers = fetch_resources(filter, RES_TYPE_SRV_CACHE_REDIS, secrets, configuration)
    return servers