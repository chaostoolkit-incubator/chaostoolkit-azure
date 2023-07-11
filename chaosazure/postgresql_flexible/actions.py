# -*- coding: utf-8 -*-
import random
import re
from typing import List

import pg8000.native
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_postgresql_flexible_management_client
from chaosazure.common import cleanse
from chaosazure.postgresql_flexible.constants import RES_TYPE_SRV_PG_FLEX
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Database
from chaosazure.common.resources.graph import fetch_resources
from chaosazure.vmss.records import Records

__all__ = ["delete_servers", "stop_servers", "restart_servers",
           "start_servers", "delete_databases", "create_databases", "delete_tables"]


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
    client = __postgresql_flexible_mgmt_client(secrets, configuration)
    server_records = Records()
    for s in servers:
        group = s['resourceGroup']
        name = s['name']
        logger.debug("Deleting server: {}".format(name))
        client.servers.begin_delete(group, name)
        server_records.add(cleanse.database_server(s))

    return server_records.output_as_dict('resources')


def stop_servers(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Stop servers at random.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stop_servers("where resourceGroup=='rg'", c, s)
    Stop all servers from the group 'rg'

    >>> stop_servers("where resourceGroup=='mygroup' and name='myname'", c, s)
    Stop the server from the group 'mygroup' having the name 'myname'

    >>> stop_servers("where resourceGroup=='mygroup' | sample 2", c, s)
    Stop two servers at random from the group 'mygroup'
    """
    logger.debug(
        "Start stop_servers: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    servers = __fetch_servers(filter, configuration, secrets)
    client = __postgresql_flexible_mgmt_client(secrets, configuration)

    server_records = Records()
    for s in servers:
        group = s['resourceGroup']
        name = s['name']
        logger.debug("Stopping server: {}".format(name))
        client.servers.begin_stop(group, name)
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
    client = __postgresql_flexible_mgmt_client(secrets, configuration)
    server_records = Records()
    for s in servers:
        group = s['resourceGroup']
        name = s['name']
        logger.debug("Restarting server: {}".format(name))
        client.servers.begin_restart(group, name)
        server_records.add(cleanse.database_server(s))

    return server_records.output_as_dict('resources')


def start_servers(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Start servers at random. Thought as a rollback action.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted all servers in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> start_servers("where resourceGroup=='rg'", c, s)
    Start all stopped servers from the group 'rg'

    >>> start_servers("where resourceGroup=='rg' and name='name'", c, s)
    Start the stopped server from the group 'rg' having the name 'name'

    >>> start_servers("where resourceGroup=='rg' | sample 2", c, s)
    Start two stopped servers at random from the group 'rg'
    """

    logger.debug(
        "Start start_servers: configuration='{}', filter='{}'".format(
            configuration, filter))

    servers = __fetch_servers(filter, configuration, secrets)
    client = __postgresql_flexible_mgmt_client(secrets, configuration)
    stopped_servers = __fetch_all_stopped_servers(client, servers)

    server_records = Records()
    for server in stopped_servers:
        logger.debug("Starting server: {}".format(server['name']))
        client.servers.begin_start(server['resourceGroup'],
                                   server['name'])

        server_records.add(cleanse.database_server(server))

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
    client = __postgresql_flexible_mgmt_client(secrets, configuration)
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
    client = __postgresql_flexible_mgmt_client(secrets, configuration)
    database_parameters = Database(charset=charset, collation=collation)
    for s in servers:
        group = s['resourceGroup']
        server_name = s['name']

        client.databases.begin_create(group, server_name, name, database_parameters)


def delete_tables(filter: str = None,
                  table_name: str = None,
                  database_name: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None,
                  key_vault_url: str = None):
    """
    Delete a table randomly from all databases in servers matching the filter.
    Could be used to introduce random failures for resilience testing.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted, all servers in the
        subscription will be considered for potential table deletion.
    table_name : str, optional
        Specific table name to delete. If this is omitted, a table will be
        selected randomly for deletion.
    database_name : str, optional
        Specific database name to delete the table from. If this is omitted,
        a database will be selected randomly from the server for table deletion.
    configuration : Configuration, optional
        Azure configuration information.
    secrets : Secrets, optional
        Azure secret information for authentication.
    key_vault_url : str, optional
        The URL to the Azure Key Vault where the secrets are stored.

    Examples
    --------
    Here are some examples of calling `delete_tables`.

    >>> delete_tables("where resourceGroup=='rg'", "users", "mydatabase",
                      c, s, "https://myvault.vault.azure.net/")
    Deletes the table 'users' from the database 'mydatabase' in all servers
    in the resource group 'rg'

    >>> delete_tables("where resourceGroup=='rg' and name='name'", None, None,
                      c, s, "https://myvault.vault.azure.net/")
    Deletes a random table from a random database in the server named 'name'
    in the resource group 'rg'

    >>> delete_tables("where resourceGroup=='rg' | sample 2", "orders",
                      "mydatabase", c, s, "https://myvault.vault.azure.net/")
    Deletes the table 'orders' from the database 'mydatabase' in two random
    servers in the resource group 'rg'
    """

    az_secrets = secrets
    cred = ClientSecretCredential(
        tenant_id=az_secrets["tenant_id"],
        client_id=az_secrets["client_id"],
        client_secret=az_secrets["client_secret"]
    )

    srvs = __fetch_servers(filter, configuration, secrets)
    if not srvs:
        logger.warning("No servers found")
        raise FailedActivity("No servers found")

    srv_records = Records()
    for srv in srvs:
        __handle_server(srv, database_name, table_name, secrets, configuration,
                        cred, key_vault_url, srv_records)

    return srv_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################


def __fetch_all_stopped_servers(client, servers) -> []:
    stopped_servers = []
    for s in servers:
        i = client.servers.get(s['resourceGroup'], s['name'])
        if i.state == 'Stopped':
            stopped_servers.append(s)
            logger.debug("Found stopped server: {}".format(s['name']))
    return stopped_servers


def __fetch_servers(filter, configuration, secrets) -> List:
    servers = fetch_resources(filter, RES_TYPE_SRV_PG_FLEX, secrets, configuration)
    if not servers:
        logger.warning("No servers found")
        raise FailedActivity("No servers found")
    else:
        logger.debug(
            "Fetched servers: {}".format(
                [s['name'] for s in servers]))
    return servers


def __postgresql_flexible_mgmt_client(secrets, configuration):
    return init_postgresql_flexible_management_client(secrets, configuration)


def __handle_server(srv,
                    database_name,
                    table_name,
                    secrets,
                    configuration,
                    cred,
                    key_vault_url,
                    srv_records):
    # Get the PostgreSQL server properties
    srv_name = srv["name"]
    resource_group = srv["resourceGroup"]
    pg_client = __postgresql_flexible_mgmt_client(secrets, configuration)
    pg_srv = pg_client.servers.get(resource_group, srv_name)

    # Construct the name of the secret containing the password
    secret_name = f"database-admin-password-{pg_srv.name}"

    # Retrieve the password from the Azure Key Vault secret
    client = SecretClient(vault_url=key_vault_url, credential=cred)
    secret_value = client.get_secret(secret_name).value

    # Retrieve all databases for the current server
    db_client = __postgresql_flexible_mgmt_client(secrets, configuration)
    db_list = db_client.databases.list_by_server(resource_group, srv_name)

    # If a database name is provided, filter the database list to include only that database
    if database_name is not None:
        db_list = [db for db in db_list if db.name == database_name]
        if not db_list:
            logger.error(
                f"Database '{database_name}' does not exist on server '{srv_name}'")
            raise FailedActivity(
                f"Database '{database_name}' does not exist on server '{srv_name}'")

    # Iterate through each database and delete the table(s)
    for db in db_list:
        dbname = db.name

        # Connect to the PostgreSQL server
        try:
            conn_str = f"host='{pg_srv.fully_qualified_domain_name}' "\
                       f"dbname='{dbname}' "\
                       f"user='{pg_srv.administrator_login}' "\
                       f"password='{secret_value}' "\
                       f"sslmode='require'"
            conn = pg8000.native.Connection(conn_str)
            __handle_db(dbname, srv_name, table_name, conn)

            srv_records.add(cleanse.database_server(srv))
            logger.debug(f"Deleted tables on server '{srv_name}'")
        except Exception:
            logger.exception(
                f"Failed to connect to database '{dbname}' on server '{srv_name}'")
            continue


def __handle_db(dbname, srv_name, table_name, conn):
    try:
        conn.run("START TRANSACTION")
        # If a table name is provided, check if the table exists and delete it
        if table_name is not None:
            tables = conn.run(
                "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_name = %s)",
                (table_name,)
            )
            exists = tables[0]
            if exists:
                conn.run(f"DROP TABLE {table_name} CASCADE")
            else:
                logger.debug(f"Table '{table_name}' does not exist on database '{dbname}'")
        # Otherwise, generate a random table name and delete it
        else:
            tables = conn.run(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_type='BASE TABLE' AND table_schema='public'"
            )
            if len(tables) > 0:
                random_table = random.choice(tables)[0]
                conn.run(f"DROP TABLE IF EXISTS {random_table} CASCADE")
                logger.debug(f"Deleted table '{random_table}' on server '{srv_name}'")
            else:
                logger.debug(f"No tables to delete on server '{srv_name}'")

        # Commit the transaction and close the connection
        conn.run("COMMIT")
        conn.close()
    except Exception:
        logger.exception(f"Failed to delete tables on server '{srv_name}'")
        if conn:
            conn.run("ROLLBACK")
            conn.close()
