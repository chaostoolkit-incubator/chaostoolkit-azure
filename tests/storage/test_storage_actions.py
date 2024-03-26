from unittest.mock import MagicMock, patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.storage.actions import (
    delete_storage_accounts,
    delete_blob_containers,
)
from azure.mgmt.storage.v2022_09_01.models import ListContainerItem

CONFIG = {"azure": {"subscription_id": "***REMOVED***"}}

SECRETS = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
}

SECRETS_CHINA = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_CHINA_CLOUD",
}

STORAGE_ACCOUNT_ALPHA = {
    "name": "chaos-storageaccount-alpha",
    "resourceGroup": "group",
}

STORAGE_ACCOUNT_BETA = {
    "name": "chaos-storageaccount-beta",
    "resourceGroup": "group",
}

container_resource_alpha = ListContainerItem()
container_resource_alpha.name = "chaos-blobcontainer-alpha"
container_resource_beta = ListContainerItem()
container_resource_beta.name = "chaos-blobcontainer-beta"
BLOB_CONTAINERS = [container_resource_alpha, container_resource_beta]


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch("chaosazure.storage.actions.__fetch_storage_accounts", autospec=True)
@patch("chaosazure.storage.actions.__storage_mgmt_client", autospec=True)
def test_delete_one_storage_account(init, fetch):
    client = MagicMock()
    init.return_value = client

    storage_accounts = [STORAGE_ACCOUNT_ALPHA]
    fetch.return_value = storage_accounts

    f = "where resourceGroup=='group' | sample 1"
    delete_storage_accounts(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.storage_accounts.delete.call_count == 1


@patch("chaosazure.storage.actions.__fetch_storage_accounts", autospec=True)
@patch("chaosazure.storage.actions.__storage_mgmt_client", autospec=True)
def test_delete_one_storage_account_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    storage_accounts = [STORAGE_ACCOUNT_ALPHA]
    fetch.return_value = storage_accounts

    f = "where resourceGroup=='group'"
    delete_storage_accounts(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.storage_accounts.delete.call_count == 1


@patch("chaosazure.storage.actions.__fetch_storage_accounts", autospec=True)
@patch("chaosazure.storage.actions.__storage_mgmt_client", autospec=True)
def test_delete_two_storage_accounts(init, fetch):
    client = MagicMock()
    init.return_value = client

    storage_accounts = [STORAGE_ACCOUNT_ALPHA, STORAGE_ACCOUNT_BETA]
    fetch.return_value = storage_accounts

    f = "where resourceGroup=='group' | sample 2"
    delete_storage_accounts(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.storage_accounts.delete.call_count == 2


@patch("chaosazure.storage.actions.fetch_resources", autospec=True)
def test_delete_storage_account_with_no_storage_accounts(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_storage_accounts(None, None, None)

    assert "No Storage accounts found" in str(x.value)


@patch("chaosazure.storage.actions.__fetch_storage_accounts", autospec=True)
@patch("chaosazure.storage.actions.__storage_mgmt_client", autospec=True)
def test_delete_one_container(init, fetch):
    client = MagicMock()
    init.return_value = client
    client.blob_containers.list.return_value = BLOB_CONTAINERS

    storage_accounts = [STORAGE_ACCOUNT_ALPHA]
    fetch.return_value = storage_accounts

    f = "where resourceGroup=='group' | sample 1"
    delete_blob_containers(f, "chaos-blobcontainer", 1, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.blob_containers.delete.call_count == 1


@patch("chaosazure.storage.actions.__fetch_storage_accounts", autospec=True)
@patch("chaosazure.storage.actions.__storage_mgmt_client", autospec=True)
def test_delete_two_container(init, fetch):
    client = MagicMock()
    init.return_value = client
    client.blob_containers.list.return_value = BLOB_CONTAINERS

    storage_accounts = [STORAGE_ACCOUNT_ALPHA]
    fetch.return_value = storage_accounts

    f = "where resourceGroup=='group' | sample 1"
    delete_blob_containers(f, "chaos-blobcontainer", 2, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.blob_containers.delete.call_count == 2


@patch("chaosazure.storage.actions.__fetch_storage_accounts", autospec=True)
@patch("chaosazure.storage.actions.__storage_mgmt_client", autospec=True)
def test_delete_blob_container_with_no_blob_containers(init, fetch):
    with pytest.raises(FailedActivity) as x:
        client = MagicMock()
        init.return_value = client
        client.blob_containers.list.return_value = BLOB_CONTAINERS

        storage_accounts = [STORAGE_ACCOUNT_ALPHA]
        fetch.return_value = storage_accounts

        f = "where resourceGroup=='group' | sample 1"
        delete_blob_containers(f, "no_results", 2, CONFIG, SECRETS)

        fetch.assert_called_with(f, CONFIG, SECRETS)
    assert "No blob containers to target found" in str(x.value)
