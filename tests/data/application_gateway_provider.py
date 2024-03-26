from chaosazure.application_gateway.constants import RES_TYPE_SRV_AG


def provide_application_gateway():
    return {
        "name": "chaos-application_gateway",
        "resourceGroup": "rg",
        "type": RES_TYPE_SRV_AG,
        "properties": {
            "provisioningState": "Succeeded",
            "operationalState": "Running",
            "requestRoutingRules": [
                {
                    "name": "appgwrule",
                    "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/requestRoutingRules/appgwrule",
                    "properties": {
                        "provisioningState": "Succeeded",
                        "ruleType": "Basic",
                        "priority": 10,
                        "httpListener": {
                            "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/httpListeners/appgwhl"
                        },
                        "backendAddressPool": {
                            "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/backendAddressPools/appgwpool"
                        },
                        "backendHttpSettings": {
                            "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/backendHttpSettingsCollection/appgwbhs"
                        },
                        "rewriteRuleSet": {
                            "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/rewriteRuleSets/rewriteRuleSet1"
                        },
                        "loadDistributionPolicy": {
                            "id": "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/applicationGateways/appgw/loadDistributionPolicies/ldp1"
                        },
                    },
                }
            ],
        },
    }
