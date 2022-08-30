# -*- coding: utf-8 -*-
import re

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.postgresql.constants import RES_TYPE_SRV_PG
from chaosazure.postgresql.actions import __postgresql_mgmt_client
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_servers", "count_servers", "describe_databases"]


def describe_servers(filter: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Describe Azure servers.

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

    servers = fetch_resources(filter, RES_TYPE_SRV_PG, secrets, configuration)
    return servers


def count_servers(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> int:
    """
    Return count of Azure servers.

    Parameters
    ----------
    filter : str
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start count_servers: configuration='{}', filter='{}'".format(
            configuration, filter))

    servers = fetch_resources(filter, RES_TYPE_SRV_PG, secrets, configuration)
    return len(servers)


def describe_databases(filter: str = None,
                       name_pattern: str = None,
                       configuration: Configuration = None,
                       secrets: Secrets = None):
    """
    Describe Azure servers.

    Parameters
    ----------
    filter : str
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    name_pattern : str
        Filter the databases. If the filter is omitted all databases in
        the server will be selected for the probe.
        Pattern example:
        'app[0-9]{3}'
    """
    logger.debug(
        "Start describe_databases: configuration='{}', filter='{}', name_pattern='{}'".format(
            configuration, filter, name_pattern))

    pattern = None
    if name_pattern:
        pattern = re.compile(name_pattern)

    servers = fetch_resources(filter, RES_TYPE_SRV_PG, secrets, configuration)
    client = __postgresql_mgmt_client(secrets, configuration)
    databases = []
    for s in servers:
        group = s['resourceGroup']
        server_name = s['name']

        for d in client.databases.list_by_server(group, server_name):
            name = d.name
            if pattern is None or pattern.search(name):
                databases.append(d.as_dict())

    return databases
