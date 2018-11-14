from chaosazure.machine.probes import count_machines

CONFIG = {
    "azure": {
        "subscription_id": "3ca1a05a-6888-4b19-bfb7-73556675e8e7",
        "resource_groups": "MC_chaosMonkeyGroup_chaosMonkeyAks_centralus"
    }
}

SECRETS = {
    "client_id": "8d997de9-9daf-43a1-98c3-04f41a64b62f",
    "client_secret": "oIAznMsOFRazS/S603EF30oDS7mivghDUQd14qjOotI=",
    "tenant_id": "9652d7c2-1ccf-4940-8151-4a92bd474ed0"
}


def test_network_action():
    filter = "where resourceGroup=~'MC_chaosMonkeyGroup_chaosMonkeyAks_centralus'"

    count_machines(configuration=CONFIG, secrets=SECRETS, filter=filter)
