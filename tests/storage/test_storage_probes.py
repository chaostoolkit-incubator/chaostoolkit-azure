from unittest.mock import MagicMock, patch


from chaosazure.storage.probes import (
    count_storage_accounts,
    describe_storage_accounts,
    count_blob_containers,
)
from azure.mgmt.storage.v2022_09_01.models import ListContainerItem

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

CONFIG = {"azure": {"subscription_id": "***REMOVED***"}}

SECRETS = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
}


@patch("chaosazure.storage.probes.fetch_resources", autospec=True)
def test_count_storage_accounts(fetch):
    resource_list = [STORAGE_ACCOUNT_ALPHA, STORAGE_ACCOUNT_BETA]
    fetch.return_value = resource_list

    count = count_storage_accounts(None, None)

    assert count == 2


@patch("chaosazure.storage.probes.fetch_resources", autospec=True)
def test_describe_storage_accounts(fetch):
    resource_list = [STORAGE_ACCOUNT_ALPHA, STORAGE_ACCOUNT_BETA]
    fetch.return_value = resource_list

    description = describe_storage_accounts(None, None)

    assert description[0]["name"] == resource_list[0]["name"]
    assert description[0]["resourceGroup"] == resource_list[0]["resourceGroup"]


@patch("chaosazure.storage.probes.fetch_resources", autospec=True)
@patch("chaosazure.storage.probes.__storage_mgmt_client", autospec=True)
def test_count_containers(init, fetch):
    client = MagicMock()
    init.return_value = client

    client.blob_containers.list.return_value = BLOB_CONTAINERS

    storage_accounts = [STORAGE_ACCOUNT_ALPHA]
    fetch.return_value = storage_accounts

    count = count_blob_containers(None, None)

    assert count == 2
