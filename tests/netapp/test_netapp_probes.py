from unittest.mock import patch


from chaosazure.netapp.probes import (
    count_netapp_volumes,
    describe_netapp_volumes,
)


NETAPP_VOLUME_ALPHA = {
    "name": "NetAppAccount/NetAppPoolName/NetAppVolumeAlpha",
    "resourceGroup": "group",
}

NETAPP_VOLUME_BETA = {
    "name": "NetAppAccount/NetAppPoolName/NetAppVolumeBeta",
    "resourceGroup": "group",
}


@patch("chaosazure.netapp.probes.fetch_resources", autospec=True)
def test_count_netapp_volumes(fetch):
    resource_list = [NETAPP_VOLUME_ALPHA, NETAPP_VOLUME_BETA]
    fetch.return_value = resource_list

    count = count_netapp_volumes(None, None)

    assert count == 2


@patch("chaosazure.netapp.probes.fetch_resources", autospec=True)
def test_describe_netapp_volumes(fetch):
    resource_list = [NETAPP_VOLUME_ALPHA]
    fetch.return_value = resource_list

    description = describe_netapp_volumes(None, None)

    assert description[0]["name"] == resource_list[0]["name"]
    assert description[0]["resourceGroup"] == resource_list[0]["resourceGroup"]
