from unittest.mock import MagicMock, patch, mock_open

import pytest
from chaoslib.exceptions import FailedActivity

import chaosazure
from chaosazure.postgresql_flexible.actions import restart_servers, stop_servers, \
    delete_servers, start_servers

from data import postgresl_flexible_provider, config_provider, secrets_provider

CONFIG = {
    "azure": {
        "subscription_id": "***REMOVED***"
    }
}

SECRETS = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***"
}

SECRETS_CHINA = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_CHINA_CLOUD"
}

SERVER_ALPHA = {
    'name': 'ServerAlpha',
    'resourceGroup': 'group'}

SERVER_BETA = {
    'name': 'ServerBeta',
    'resourceGroup': 'group'}


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_delete_one_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_delete.call_count == 1


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_delete_one_server_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_servers(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.servers.begin_delete.call_count == 1


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_delete_two_servers(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA, SERVER_BETA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_delete.call_count == 2


@patch('chaosazure.postgresql_flexible.actions.fetch_resources', autospec=True)
def test_delete_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_servers(None, None, None)

    assert "No servers found" in str(x.value)


@patch('chaosazure.postgresql_flexible.actions.fetch_resources', autospec=True)
def test_stop_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_servers(None, None, None)

    assert "No servers found" in str(x.value)


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_stop_one_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_stop.call_count == 1


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_stop_two_servers(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA, SERVER_BETA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_stop.call_count == 2


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_restart_one_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    restart_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_restart.call_count == 1


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_restart_two_server(init, fetch):
    client = MagicMock()
    init.return_value = client

    servers = [SERVER_ALPHA, SERVER_BETA]
    fetch.return_value = servers

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    restart_servers(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.servers.begin_restart.call_count == 2


@patch('chaosazure.postgresql_flexible.actions.fetch_resources', autospec=True)
def test_restart_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_servers(None, None, None)

    assert "No servers found" in str(x.value)


@patch('chaosazure.postgresql_flexible.actions.fetch_resources', autospec=True)
def test_start_server_with_no_servers(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_servers()

    assert "No servers found" in str(x.value)


@patch('chaosazure.postgresql_flexible.actions.__fetch_servers', autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__fetch_all_stopped_servers',
       autospec=True)
@patch('chaosazure.postgresql_flexible.actions.__postgresql_flexible_mgmt_client', autospec=True)
def test_start_server(init, fetch_stopped, fetch_all):
    client = MagicMock()
    init.return_value = client
