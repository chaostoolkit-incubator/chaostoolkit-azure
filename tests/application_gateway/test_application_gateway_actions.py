from unittest.mock import MagicMock, patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.application_gateway.actions import (
    delete_application_gateways,
    start_application_gateways,
    stop_application_gateways,
)


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

APPLICATION_GATEWAY_ALPHA = {
    "name": "ApplicationGatewayAlpha",
    "resourceGroup": "group",
}

APPLICATION_GATEWAY_BETA = {
    "name": "ApplicationGatewayBeta",
    "resourceGroup": "group",
}


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_delete_one_application_gateway(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_application_gateways(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.application_gateways.begin_delete.call_count == 1


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_delete_one_application_gateway_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_application_gateways(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.application_gateways.begin_delete.call_count == 1


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_delete_two_application_gateways(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA, APPLICATION_GATEWAY_BETA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_application_gateways(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.application_gateways.begin_delete.call_count == 2


@patch("chaosazure.application_gateway.actions.fetch_resources", autospec=True)
def test_delete_application_gateway_with_no_application_gateways(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_application_gateways(None, None, None)

    assert "No application gateways found" in str(x.value)


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_start_one_application_gateway(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    start_application_gateways(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.application_gateways.begin_start.call_count == 1


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_start_two_application_gateways(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA, APPLICATION_GATEWAY_BETA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    start_application_gateways(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.application_gateways.begin_start.call_count == 2


@patch("chaosazure.application_gateway.actions.fetch_resources", autospec=True)
def test_start_application_gateway_with_no_application_gateways(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_application_gateways(None, None, None)

    assert "No application gateways found" in str(x.value)


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_stop_one_application_gateway(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_application_gateways(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.application_gateways.begin_stop.call_count == 1


@patch(
    "chaosazure.application_gateway.actions.__fetch_application_gateways",
    autospec=True,
)
@patch(
    "chaosazure.application_gateway.actions.__network_mgmt_client",
    autospec=True,
)
def test_stop_two_application_gateways(init, fetch):
    client = MagicMock()
    init.return_value = client

    application_gateways = [APPLICATION_GATEWAY_ALPHA, APPLICATION_GATEWAY_BETA]
    fetch.return_value = application_gateways

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_application_gateways(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.application_gateways.begin_stop.call_count == 2


@patch("chaosazure.application_gateway.actions.fetch_resources", autospec=True)
def test_stop_application_gateway_with_no_application_gateways(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_application_gateways(None, None, None)

    assert "No application gateways found" in str(x.value)
