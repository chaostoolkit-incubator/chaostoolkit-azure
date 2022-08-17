# -*- coding: utf-8 -*-
import re

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_postgresql_management_client
from chaosazure.common import cleanse
from chaosazure.postgresql.constants import RES_TYPE_SRV_PG
from azure.mgmt.rdbms.postgresql.models import Database
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["delete_servers", "restart_servers", "delete_databases", "create_databases"]

from chaosazure.vmss.records import Records


def delete_servers(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Delete servers at random.

    **Be aware**: Deleting a server is an invasive action. You will not be
    able to recover the server once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_servers("where resourceGroup=='rg'", c, s)
    Delete all servers from the group 'rg'

    >>> delete_servers("where resourceGroup=='rg' and name='name'", c, s)
    Delete the server from the group 'rg' having the name 'name'

    >>> delete_servers("where resourceGroup=='rg' | sample 2", c, s)
    Delete two servers at random from the group 'rg'
    """
    logger.debug(
        "Start delete_servers: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    servers = __fetch_servers(filter, configuration, secrets)
    client = __postgresql_mgmt_client(secrets, configuration)
    server_records = Records()
    for s in servers:
        group = s['resourceGroup']
        name = s['name']
        logger.debug("Deleting server: {}".format(name))
        client.servers.begin_delete(group, name)
        server_records.add(cleanse.database_server(s))

    return server_records.output_as_dict('resources')


def restart_servers(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Restart servers at random.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> restart_servers("where resourceGroup=='rg'", c, s)
    Restart all servers from the group 'rg'

    >>> restart_servers("where resourceGroup=='rg' and name='name'", c, s)
    Restart the server from the group 'rg' having the name 'name'

    >>> restart_servers("where resourceGroup=='rg' | sample 2", c, s)
    Restart two servers at random from the group 'rg'
    """
    logger.debug(
        "Start restart_servers: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    servers = __fetch_servers(filter, configuration, secrets)
    client = __postgresql_mgmt_client(secrets, configuration)
    server_records = Records()
    for s in servers:
        group = s['resourceGroup']
        name = s['name']
        logger.debug("Restarting server: {}".format(name))
        client.servers.begin_restart(group, name)
        server_records.add(cleanse.database_server(s))

    return server_records.output_as_dict('resources')


def delete_databases(filter: str = None,
                     name_pattern: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Delete databases at random.

    **Be aware**: Deleting a database is an invasive action. You will not be
    able to recover the database once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all databases
        of all servers in the subscription will be selected
        as potential chaos candidates.

    name_pattern : str, optional
        Filter the databases. If the filter is omitted all databases in
        the server will be selected for the probe.
        Pattern example:
        'app[0-9]{3}'

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_databases("where resourceGroup=='rg'", 'chaos-*', c, s)
    Delete all database named 'chaos-*' in all servers from the group 'rg'

    >>> delete_databases("where resourceGroup=='rg' and name='name'", 'chaos-test', c, s)
    Delete all database named 'chaos-*' the server from the group 'rg' having the name 'name'
    """
    logger.debug(
        "Start delete_databases: "
        "configuration='{}', filter='{}', name_pattern='{}'".format(
            configuration, filter, name_pattern))

    pattern = None
    if name_pattern:
        pattern = re.compile(name_pattern)

    servers = __fetch_servers(filter, configuration, secrets)
    client = __postgresql_mgmt_client(secrets, configuration)
    database_records = Records()
    for s in servers:
        group = s['resourceGroup']
        server_name = s['name']

        for d in client.databases.list_by_server(group, server_name):
            name = d.name
            if pattern is None or pattern.search(name):
                client.databases.begin_delete(group, server_name, name)
                database_records.add(cleanse.database_database(d.as_dict()))

        logger.debug("Deleting database: {}/{}".format(server_name, name))

    return database_records.output_as_dict('resources')


def create_databases(filter: str = None,
                     name: str = None,
                     charset: str = None,
                     collation: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Delete databases at random.

    **Be aware**: Deleting a database is an invasive action. You will not be
    able to recover the database once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all databases
        of all servers in the subscription will be selected
        as potential chaos candidates.

    name : str, required
        The name of the database to create.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> create_databases("where resourceGroup=='rg'", 'chaos-test', c, s)
    Creating database named 'chaos-test' in all servers from the group 'rg'

    >>> create_databases("where resourceGroup=='rg' and name='name'", 'chaos-test', c, s)
    Creating database named 'chaos-test' the server from the group 'rg' having the name 'name'
    """
    logger.debug(
        "Start create_databases: "
        "configuration='{}', filter='{}', name='{}'".format(configuration, filter, name))

    servers = __fetch_servers(filter, configuration, secrets)
    client = __postgresql_mgmt_client(secrets, configuration)
    database_parameters = Database(charset=charset, collation=collation)
    for s in servers:
        group = s['resourceGroup']
        server_name = s['name']

        client.databases.begin_create_or_update(group, server_name, name, database_parameters)


###############################################################################
# Private helper functions
###############################################################################


def __fetch_servers(filter, configuration, secrets) -> []:
    servers = fetch_resources(filter, RES_TYPE_SRV_PG, secrets, configuration)
    if not servers:
        logger.warning("No servers found")
        raise FailedActivity("No servers found")
    else:
        logger.debug(
            "Fetched servers: {}".format(
                [s['name'] for s in servers]))
    return servers


def __postgresql_mgmt_client(secrets, configuration):
    return init_postgresql_management_client(secrets, configuration)
