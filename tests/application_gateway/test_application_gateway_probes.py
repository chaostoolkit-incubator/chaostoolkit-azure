from unittest.mock import patch


from chaosazure.application_gateway.probes import (
    count_application_gateways,
    describe_application_gateways,
)


resource = {"name": "chaos-application_gateway", "resourceGroup": "rg"}

route_resource = {
    "name": "appgwrule",
    "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/requestRoutingRules/appgwrule",
    "properties": {"provisioningState": "Succeeded", "ruleType": "Basic"},
}


@patch("chaosazure.application_gateway.probes.fetch_resources", autospec=True)
def test_count_application_gateways(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    count = count_application_gateways(None, None)

    assert count == 1


@patch("chaosazure.application_gateway.probes.fetch_resources", autospec=True)
def test_describe_application_gateways(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    description = describe_application_gateways(None, None)

    assert description[0]["name"] == resource["name"]
    assert description[0]["resourceGroup"] == resource["resourceGroup"]
