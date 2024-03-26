from unittest.mock import MagicMock, patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.postgresql_flexible.actions import (
    restart_servers,
    stop_servers,
    delete_servers,
    start_servers,
    delete_tables,
)


CONFIG = {"azure_subscription_id": "***REMOVED***"}

SECRETS = {
    "azure": {
        "client_id": "***REMOVED***",
        "client_secret": "***REMOVED***",
        "tenant_id": "***REMOVED***",
        "azure_cloud": "AZURE_PUBLIC_CLOUD",
    }
}

SECRETS_CHINA = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_CHINA_CLOUD",
}

SERVER_ALPHA = {
    "name": "ServerAlpha",
    "resourceGroup": "group",
    "fully_qualified_domain_name": "server_alpha.fully_qualified_domain_name",
    "administrator_login": "server_alpha.administrator_login",
}

SERVER_BETA = {"name": "ServerBeta", "resourceGroup": "group"}


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_delete_one_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_delete.call_count == 1


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_delete_one_server_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_servers(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.servers.begin_delete.call_count == 1


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_delete_two_servers(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA, SERVER_BETA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_delete.call_count == 2


@patch("chaosazure.postgresql_flexible.actions.fetch_resources", autospec=True)
def test_delete_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_servers(None, None, None)

    assert "No servers found" in str(x.value)


@patch("chaosazure.postgresql_flexible.actions.fetch_resources", autospec=True)
def test_stop_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_servers(None, None, None)

    assert "No servers found" in str(x.value)


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_stop_one_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_stop.call_count == 1


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_stop_two_servers(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA, SERVER_BETA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_stop.call_count == 2


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_restart_one_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    restart_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_restart.call_count == 1


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_restart_two_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA, SERVER_BETA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    restart_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_restart.call_count == 2


@patch("chaosazure.postgresql_flexible.actions.fetch_resources", autospec=True)
def test_restart_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_servers(None, None, None)

    assert "No servers found" in str(x.value)


@patch("chaosazure.postgresql_flexible.actions.fetch_resources", autospec=True)
def test_start_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_servers()

    assert "No servers found" in str(x.value)


@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__fetch_all_stopped_servers",
    autospec=True,
)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
def test_start_server(init, fetch_stopped, fetch_all):
    client = MagicMock()
    init.return_value = client


@patch(
    "chaosazure.postgresql_flexible.actions.ClientSecretCredential",
    autospec=True,
)
@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
@patch("chaosazure.postgresql_flexible.actions.SecretClient", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.pg8000.native.Connection",
    autospec=True,
)
def test_delete_tables_unknown_table(
    connect_mock: MagicMock,
    secret_client_mock,
    init_mock,
    fetch_servers_mock,
    ClientSecretCredential_mock,
):
    # Create a mock for the ClientSecretCredential
    ClientSecretCredential_mock.return_value = MagicMock()

    # Mock Azure client
    client_mock = MagicMock()
    init_mock.return_value = client_mock

    # Use SERVER_ALPHA as a mock server
    server_alpha = MagicMock()
    server_alpha.fully_qualified_domain_name = SERVER_ALPHA[
        "fully_qualified_domain_name"
    ]
    server_alpha.administrator_login = SERVER_ALPHA["administrator_login"]
    server_alpha.name = SERVER_ALPHA["name"]
    servers = [server_alpha]
    client_mock.servers.get.return_value = server_alpha
    fetch_servers_mock.return_value = servers

    # Mock secret value returned by SecretClient
    secret_value_mock = MagicMock()
    secret_value_mock.value = "secret_value"
    # Configure SecretClient to return the mocked secret value
    secret_client_mock.return_value = MagicMock(
        get_secret=MagicMock(return_value=secret_value_mock)
    )

    # Simulate a list of databases with a single database
    db_mock = MagicMock()
    db_mock.name = "mydatabase"
    db_client_mock = MagicMock()
    db_client_mock.list_by_server.return_value = [db_mock]
    client_mock.databases = db_client_mock

    # Simulate a successful connection to the database
    conn = connect_mock.return_value
    # Configure the cursor mock to return False when checking table existence
    conn.run.side_effect = [None, [False], None, None]
    conn.close = MagicMock()

    # Filter for the resource group and non-existent table name
    f = "where resourceGroup=='myresourcegroup'"
    table_name = "nonexistent_table"
    database_name = None

    # Call the function under test with the necessary parameters
    delete_tables(
        f, table_name, database_name, CONFIG, SECRETS["azure"], "key_vault_url"
    )

    # Verify calls to different functions with appropriate arguments
    fetch_servers_mock.assert_called_with(f, CONFIG, SECRETS["azure"])
    assert client_mock.servers.get.call_count == 1

    # Verify the correct connection parameters were used
    host = server_alpha.fully_qualified_domain_name
    login = server_alpha.administrator_login
    params = f"host='{host}' dbname='mydatabase' user='{login}' password='secret_value' sslmode='require'"
    connect_mock.assert_called_once_with(params)

    # Verify the table existence check query was executed
    query = (
        "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = %s)"
    )
    conn.run.assert_any_call(query, (table_name,))

    # Verify that the correct functions were called the right number of times
    assert (
        secret_client_mock.call_count == 1
    )  # Check that the SecretClient method is called once.
    assert connect_mock.call_count == 1  # Connection should be made once
    assert conn.run.call_count == 3  # Check table existence
    assert conn.close.call_count == 1  # Connection should be closed once
    assert client_mock.servers.begin_delete.call_count == 0  # No table deleted


@patch(
    "chaosazure.postgresql_flexible.actions.ClientSecretCredential",
    autospec=True,
)
@patch("chaosazure.postgresql_flexible.actions.__fetch_servers", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client",
    autospec=True,
)
@patch("chaosazure.postgresql_flexible.actions.SecretClient", autospec=True)
@patch(
    "chaosazure.postgresql_flexible.actions.pg8000.native.Connection",
    autospec=True,
)
def test_delete_tables_existing_table(
    connect_mock: MagicMock,
    secret_client_mock,
    init_mock,
    fetch_servers_mock,
    ClientSecretCredential_mock,
):
    # Create a mock for the ClientSecretCredential
    ClientSecretCredential_mock.return_value = MagicMock()

    # Mock Azure client
    client_mock = MagicMock()
    init_mock.return_value = client_mock

    # Use SERVER_ALPHA as a mock server
    server_alpha = MagicMock()
    server_alpha.fully_qualified_domain_name = SERVER_ALPHA[
        "fully_qualified_domain_name"
    ]
    server_alpha.administrator_login = SERVER_ALPHA["administrator_login"]
    server_alpha.name = SERVER_ALPHA["name"]
    servers = [server_alpha]
    client_mock.servers.get.return_value = server_alpha
    fetch_servers_mock.return_value = servers

    # Mock secret value returned by SecretClient
    secret_value_mock = MagicMock()
    secret_value_mock.value = "secret_value"
    # Configure SecretClient to return the mocked secret value
    secret_client_mock.return_value = MagicMock(
        get_secret=MagicMock(return_value=secret_value_mock)
    )

    # Simulate a list of databases with a single database
    db_mock = MagicMock()
    db_mock.name = "mydatabase"
    db_client_mock = MagicMock()
    db_client_mock.list_by_server.return_value = [db_mock]
    client_mock.databases = db_client_mock

    # Simulate a successful connection to the database
    conn = connect_mock.return_value
    # Configure the cursor mock to return True when checking table existence
    conn.run.side_effect = [None, [True], None, None]

    # Filter for the resource group and existing table name
    f = "where resourceGroup=='myresourcegroup'"
    table_name = "existing_table"
    database_name = None

    # Call the function under test with the necessary parameters
    delete_tables(
        f, table_name, database_name, CONFIG, SECRETS["azure"], "key_vault_url"
    )

    # Verify calls to different functions with appropriate arguments
    fetch_servers_mock.assert_called_with(f, CONFIG, SECRETS["azure"])
    assert client_mock.servers.get.call_count == 1

    # Verify the correct connection parameters were used
    host = server_alpha.fully_qualified_domain_name
    login = server_alpha.administrator_login
    params = f"host='{host}' dbname='mydatabase' user='{login}' password='secret_value' sslmode='require'"
    connect_mock.assert_any_call(params)

    # Verify the table existence check query was executed
    query = (
        "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = %s)"
    )
    conn.run.assert_any_call(query, (table_name,))

    # Check that the SecretClient method is called once.
    assert secret_client_mock.call_count == 1
    # No connection should be made
    assert connect_mock.call_count == 1  # No connection should be made
    # Check table existence and table deletion
    assert conn.run.call_count == 4
    # Verify that we are checking the existence of the table
    assert conn.run.call_args_list[1][0][0] == (
        "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = %s)"
    )
    # Verify that we are sending a command to drop the table
    assert (
        conn.run.call_args_list[2][0][0] == f"DROP TABLE {table_name} CASCADE"
    )
