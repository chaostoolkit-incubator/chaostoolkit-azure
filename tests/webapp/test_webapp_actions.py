from unittest.mock import patch, MagicMock

from chaosazure.webapp.actions import stop_webapp, restart_webapp, \
    start_webapp, delete_webapp

CONFIG = {
    "azure": {
        "subscription_id": "X"
    }
}

SECRETS = {
    "client_id": "X",
    "client_secret": "X",
    "tenant_id": "X"
}

resource = {
    'name': 'chaos-webapp',
    'resourceGroup': 'rg'}


@patch('chaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('chaosazure.webapp.actions.init_website_management_client', autospec=True)
def test_stop_webapp(init, fetch):
    client = MagicMock()
    init.return_value = client
    resource_list = [resource]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    stop_webapp(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    client.web_apps.stop.assert_called_with(resource['resourceGroup'],
                                            resource['name'])


@patch('chaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('chaosazure.webapp.actions.init_website_management_client', autospec=True)
def test_restart_webapp(init, fetch):
    client = MagicMock()
    init.return_value = client
    resource_list = [resource]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    restart_webapp(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    client.web_apps.restart.assert_called_with(resource['resourceGroup'],
                                            resource['name'])


@patch('chaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('chaosazure.webapp.actions.init_website_management_client', autospec=True)
def test_start_webapp(init, fetch):
    client = MagicMock()
    init.return_value = client
    resource_list = [resource]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    start_webapp(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    client.web_apps.start.assert_called_with(resource['resourceGroup'],
                                               resource['name'])


@patch('chaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('chaosazure.webapp.actions.init_website_management_client', autospec=True)
def test_delete_webapp(init, fetch):
    client = MagicMock()
    init.return_value = client
    resource_list = [resource]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    delete_webapp(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    client.web_apps.delete.assert_called_with(resource['resourceGroup'],
                                             resource['name'])
