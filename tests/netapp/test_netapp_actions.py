from unittest.mock import MagicMock, patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.netapp.actions import delete_netapp_volumes

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

NETAPP_VOLUME_ALPHA = {
    "name": "NetAppAccount/NetAppPoolName/NetAppVolumeAlpha",
    "resourceGroup": "group",
}

NETAPP_VOLUME_BETA = {
    "name": "NetAppAccount/NetAppPoolName/NetAppVolumeBeta",
    "resourceGroup": "group",
}


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch("chaosazure.netapp.actions.__fetch_netapp_volumes", autospec=True)
@patch("chaosazure.netapp.actions.__netapp_mgmt_client", autospec=True)
def test_delete_one_netapp_volume(init, fetch):
    client = MagicMock()
    init.return_value = client

    netapp_volumes = [NETAPP_VOLUME_ALPHA]
    fetch.return_value = netapp_volumes

    f = "where resourceGroup=='group' | sample 1"
    delete_netapp_volumes(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.volumes.begin_delete.call_count == 1


@patch("chaosazure.netapp.actions.__fetch_netapp_volumes", autospec=True)
@patch("chaosazure.netapp.actions.__netapp_mgmt_client", autospec=True)
def test_delete_one_netapp_volume_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    netapp_volumes = [NETAPP_VOLUME_ALPHA]
    fetch.return_value = netapp_volumes

    f = "where resourceGroup=='group'"
    delete_netapp_volumes(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.volumes.begin_delete.call_count == 1


@patch("chaosazure.netapp.actions.__fetch_netapp_volumes", autospec=True)
@patch("chaosazure.netapp.actions.__netapp_mgmt_client", autospec=True)
def test_delete_two_netapp_volumes(init, fetch):
    client = MagicMock()
    init.return_value = client

    netapp_volumes = [NETAPP_VOLUME_ALPHA, NETAPP_VOLUME_BETA]
    fetch.return_value = netapp_volumes

    f = "where resourceGroup=='group' | sample 2"
    delete_netapp_volumes(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.volumes.begin_delete.call_count == 2


@patch("chaosazure.netapp.actions.fetch_resources", autospec=True)
def test_delete_netapp_volume_with_no_netapp_volumes(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_netapp_volumes(None, None, None)

    assert "No Netapp volumes found" in str(x.value)
