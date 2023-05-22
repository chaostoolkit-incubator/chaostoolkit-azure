# -*- coding: utf-8 -*-
import re
import random
import psycopg2

from azure.identity import ClientSecretCredential
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.keyvault.secrets import SecretClient

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_postgresql_flexible_management_client
from chaosazure.common import cleanse
from chaosazure.postgresql_flexible.constants import RES_TYPE_SRV_PG_FLEX
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Database
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["delete_servers", "stop_servers", "restart_servers",
           "start_servers", "delete_databases", "create_databases", "delete_tables"]

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

def delete_tables(filter: str = None,
                  table_name: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None,
                  key_vault_url: str = None):
    """
    Delete a table randomly from all servers matching the filter. Could be used to introduce random failures for resilience testing.

    Parameters
    ----------
    filter : str, optional
        Filter the servers. If the filter is omitted, all servers in
        the subscription will be considered for potential table deletion.

    table_name : str, optional
        Specific table name to delete. If this is omitted, a table will be selected randomly for deletion.

    configuration : Configuration, optional
        Azure configuration information.

    secrets : Secrets, optional
        Azure secret information for authentication.

    key_vault_url : str, optional
        The URL to the Azure Key Vault where the secrets are stored.

    Examples
    --------
    Here are some examples of calling `delete_tables`. 

    >>> delete_tables("where resourceGroup=='rg'", "users", c, s, "https://myvault.vault.azure.net/")
    Deletes the table 'users' from all servers in the resource group 'rg'

    >>> delete_tables("where resourceGroup=='rg' and name='name'", None, c, s, "https://myvault.vault.azure.net/")
    Deletes a random table from the server named 'name' in the resource group 'rg'

    >>> delete_tables("where resourceGroup=='rg' | sample 2", "orders", c, s, "https://myvault.vault.azure.net/")
    Deletes the table 'orders' from two random servers in the resource group 'rg'
    """
    # Retrieve the Azure secrets from the plan
    azure_subscription_id = configuration["azure_subscription_id"]
    azure_secrets = secrets
    credential = ClientSecretCredential(
        tenant_id=azure_secrets["tenant_id"],
        client_id=azure_secrets["client_id"],
        client_secret=azure_secrets["client_secret"]
    )

    # Fetch the servers matching the filter
    servers = __fetch_servers(filter, configuration, secrets)
    if not servers:
        logger.warning("No servers found")
        raise FailedActivity("No servers found")

    server_records = Records()
    for server in servers:
        # Get the PostgreSQL server properties
        server_name = server["name"]
        resource_group_name = server["resourceGroup"]
        postgresql_client = __postgresql_flexible_mgmt_client(secrets, configuration)
        pg_server = postgresql_client.servers.get(
            resource_group_name=resource_group_name,
            server_name=server_name
        )

        # Construct the name of the secret containing the password
        secret_name = f"database-admin-password-{pg_server.name}"

        # Retrieve the password from the Azure Key Vault secret
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret_value = client.get_secret(secret_name).value

        # Retrieve all databases for the current server
        db_client = __postgresql_flexible_mgmt_client(secrets, configuration)
        db_list = db_client.databases.list_by_server(resource_group_name, server_name)

        # Iterate through each database and delete the table(s)
        for db in db_list:
            dbname = db.name

            # Connect to the PostgreSQL server
            try:
                conn_str = f"host='{pg_server.fully_qualified_domain_name}' dbname='{dbname}' user='{pg_server.administrator_login}' password='{secret_value}' sslmode='require'"
                conn = psycopg2.connect(conn_str)
                cursor = conn.cursor()

                try:
                    # If a table name is provided, check if the table exists and delete it
                    if table_name is not None:
                        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s)", (table_name,))
                        exists = cursor.fetchone()[0]
                        if exists:
                            cursor.execute(f"DROP TABLE {table_name} CASCADE")
                            deleted_tables = {server_name: table_name}
                        else:
                            logger.debug(f"Table '{table_name}' does not exist on database '{dbname}'")
                            deleted_tables = {}
                    # Otherwise, generate a random table name and delete it    
                    else:
                        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public'")
                        tables = cursor.fetchall()
                        if len(tables) > 0:
                            random_table = random.choice(tables)[0]
                            cursor.execute(f"DROP TABLE IF EXISTS {random_table} CASCADE")
                            deleted_tables = {server_name: random_table}
                            logger.debug(f"Deleted table '{random_table}' on server '{server_name}'")
                        else:
                            logger.debug(f"No tables to delete on server '{server_name}'")
                            deleted_tables = {}

                    # Commit the transaction and close the connection
                    conn.commit()
                    cursor.close()
                    conn.close()

                    server_records.add(cleanse.database_server(server))
                    logger.debug(f"Deleted tables on server '{server_name}'")
                except Exception as e:
                    logger.exception(
                        f"Failed to delete tables on server '{server_name}'")
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.rollback()
                        conn.close()
            except Exception as e:
                logger.exception(
                    f"Failed to connect to database '{dbname}' on server '{server_name}'")
                continue

    return server_records.output_as_dict('resources')


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


def __fetch_servers(filter, configuration, secrets) -> []:
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
    
