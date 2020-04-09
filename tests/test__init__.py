import os

import pytest
from chaosazure import __get_cloud_env_by_name, init_client,\
    init_resource_graph_client
from chaoslib.exceptions import InterruptExecution    
from logzero import logger
from unittest.mock import MagicMock, patch, ANY
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD, \
    AZURE_US_GOV_CLOUD, AZURE_GERMAN_CLOUD, AZURE_CHINA_CLOUD

CONFIG = {
    "azure": {
        "subscription_id": "***REMOVED***"
    }
}

FLAT_CONFIG_FROM_EN = {
    "azure_subscription_id": {
        "type": "env",
        "key": "SUBSCRIPTION_ID"
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

SECRETS_GERMANY = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_GERMAN_CLOUD"
}

SECRETS_USGOV = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_US_GOV_CLOUD"
}

SECRETS_PUBLIC = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_PUBLIC_CLOUD"
}

SECRETS_PUBLIC_TOKEN = {
    "client_id": "***REMOVED***",
    "access_token": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_PUBLIC_CLOUD"
}

SECRETS_BAD_CLOUD = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "LDJFSLULAJDLDSJFSL"
}


def test_get_env_by_name_default():
    parsed_base_url = __get_cloud_env_by_name(
        SECRETS.get("azure_cloud")).endpoints.resource_manager
    assert parsed_base_url == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


def test_get_env_by_name_china():
    parsed_base_url = __get_cloud_env_by_name(
        SECRETS_CHINA.get("azure_cloud")).endpoints.resource_manager
    assert parsed_base_url == AZURE_CHINA_CLOUD.endpoints.resource_manager


def test_get_env_by_name_public():
    parsed_base_url = __get_cloud_env_by_name(
        SECRETS_PUBLIC.get("azure_cloud")).endpoints.resource_manager
    assert parsed_base_url == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


def test_get_env_by_name_germany():
    parsed_base_url = __get_cloud_env_by_name(
        SECRETS_GERMANY.get("azure_cloud")).endpoints.resource_manager
    assert parsed_base_url == AZURE_GERMAN_CLOUD.endpoints.resource_manager


def test_get_env_by_name_us():
    parsed_base_url = __get_cloud_env_by_name(
        SECRETS_USGOV.get("azure_cloud")).endpoints.resource_manager
    assert parsed_base_url == AZURE_US_GOV_CLOUD.endpoints.resource_manager


def test_get_env_by_name_bad():
    parsed_base_url = __get_cloud_env_by_name(
        SECRETS_BAD_CLOUD.get("azure_cloud")).endpoints.resource_manager
    assert parsed_base_url == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


def test_get_env_by_name_bad2():
    parsed_base_url = __get_cloud_env_by_name(None).endpoints.resource_manager
    assert parsed_base_url == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


def test_get_env_by_name_bad3():
    parsed_base_url = __get_cloud_env_by_name(5).endpoints.resource_manager
    assert parsed_base_url == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
def test_credential_default(spcred):
    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS.get("client_id"),
        secret=SECRETS.get('client_secret'),
        tenant=SECRETS.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS.get('azure_cloud')))


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
def test_credential_china(spcred):
    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_CHINA, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_CHINA.get("client_id"),
        secret=SECRETS_CHINA.get('client_secret'),
        tenant=SECRETS_CHINA.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_CHINA.get('azure_cloud')))


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
def test_credential_bad(spcred):
    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_BAD_CLOUD, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_BAD_CLOUD.get("client_id"),
        secret=SECRETS_BAD_CLOUD.get('client_secret'),
        tenant=SECRETS_BAD_CLOUD.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_BAD_CLOUD.get('azure_cloud')))


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_china(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_CHINA, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_CHINA.get("client_id"),
        secret=SECRETS_CHINA.get('client_secret'),
        tenant=SECRETS_CHINA.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_CHINA.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS_CHINA.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_default(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS.get("client_id"),
        secret=SECRETS.get('client_secret'),
        tenant=SECRETS.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_bad(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_BAD_CLOUD, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_BAD_CLOUD.get("client_id"),
        secret=SECRETS_BAD_CLOUD.get('client_secret'),
        tenant=SECRETS_BAD_CLOUD.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_BAD_CLOUD.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS_BAD_CLOUD.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_germany(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_GERMANY, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_GERMANY.get("client_id"),
        secret=SECRETS_GERMANY.get('client_secret'),
        tenant=SECRETS_GERMANY.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_GERMANY.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS_GERMANY.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_public(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_PUBLIC, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_PUBLIC.get("client_id"),
        secret=SECRETS_PUBLIC.get('client_secret'),
        tenant=SECRETS_PUBLIC.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_PUBLIC.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS_PUBLIC.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_usgov(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS_USGOV, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS_USGOV.get("client_id"),
        secret=SECRETS_USGOV.get('client_secret'),
        tenant=SECRETS_USGOV.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_USGOV.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS_USGOV.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ResourceGraphClient', autospec=True)
def test_init_rg_client_china(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_resource_graph_client(SECRETS_CHINA)

    spcred.assert_called_with(
        client_id=SECRETS_CHINA.get("client_id"),
        secret=SECRETS_CHINA.get('client_secret'),
        tenant=SECRETS_CHINA.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_CHINA.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        base_url=__get_cloud_env_by_name(
            SECRETS_CHINA.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ResourceGraphClient', autospec=True)
def test_init_rg_client_default(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_resource_graph_client(SECRETS)

    spcred.assert_called_with(
        client_id=SECRETS.get("client_id"),
        secret=SECRETS.get('client_secret'),
        tenant=SECRETS.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        base_url=__get_cloud_env_by_name(
            SECRETS.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ResourceGraphClient', autospec=True)
def test_init_rg_client_bad(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_resource_graph_client(SECRETS_BAD_CLOUD)

    spcred.assert_called_with(
        client_id=SECRETS_BAD_CLOUD.get("client_id"),
        secret=SECRETS_BAD_CLOUD.get('client_secret'),
        tenant=SECRETS_BAD_CLOUD.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_BAD_CLOUD.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        base_url=__get_cloud_env_by_name(
            SECRETS_BAD_CLOUD.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ResourceGraphClient', autospec=True)
def test_init_rg_client_germany(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_resource_graph_client(SECRETS_GERMANY)

    spcred.assert_called_with(
        client_id=SECRETS_GERMANY.get("client_id"),
        secret=SECRETS_GERMANY.get('client_secret'),
        tenant=SECRETS_GERMANY.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_GERMANY.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        base_url=__get_cloud_env_by_name(
            SECRETS_GERMANY.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ResourceGraphClient', autospec=True)
def test_init_rg_client_public(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_resource_graph_client(SECRETS_PUBLIC)

    spcred.assert_called_with(
        client_id=SECRETS_PUBLIC.get("client_id"),
        secret=SECRETS_PUBLIC.get('client_secret'),
        tenant=SECRETS_PUBLIC.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_PUBLIC.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        base_url=__get_cloud_env_by_name(
            SECRETS_PUBLIC.get("azure_cloud")).
            endpoints.resource_manager)


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
@patch('chaosazure.ResourceGraphClient', autospec=True)
def test_init_rg_client_usgov(cmclient, spcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    spcred.return_value = cred

    init_resource_graph_client(SECRETS_USGOV)

    spcred.assert_called_with(
        client_id=SECRETS_USGOV.get("client_id"),
        secret=SECRETS_USGOV.get('client_secret'),
        tenant=SECRETS_USGOV.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS_USGOV.get('azure_cloud')))

    cmclient.assert_called_with(
        credentials=ANY,
        base_url=__get_cloud_env_by_name(
            SECRETS_USGOV.get("azure_cloud")).
            endpoints.resource_manager)

@patch('chaosazure.AADTokenCredentials', autospec=True)
@patch('chaosazure.ComputeManagementClient', autospec=True)
def test_init_client_public_token_credentials(cmclient, aadcred):
    client = MagicMock()
    cmclient.return_value = client

    cred = MagicMock()
    aadcred.return_value = cred

    init_client(SECRETS_PUBLIC_TOKEN, CONFIG)

    aadcred.assert_called_with(
        dict(accessToken=SECRETS_PUBLIC_TOKEN.get('access_token')),
        client_id=SECRETS_PUBLIC_TOKEN.get('client_id'))

    cmclient.assert_called_with(
        credentials=ANY,
        subscription_id=CONFIG['azure']['subscription_id'],
        base_url=__get_cloud_env_by_name(
            SECRETS_PUBLIC.get("azure_cloud")).
            endpoints.resource_manager)

@patch('chaosazure.logger', autospec=True)
def test_access_token_or_client_secret_must_be_set(logger: logger):
    with pytest.raises(InterruptExecution) as execinfo:  
        init_client(dict(), CONFIG) 

    assert str(execinfo.value) == 'Authentication to Azure requires a client secret or an access token'


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
def test_credential_using_nested_config(spcred):
    cred = MagicMock()
    spcred.return_value = cred

    init_client(SECRETS, CONFIG)

    spcred.assert_called_with(
        client_id=SECRETS.get("client_id"),
        secret=SECRETS.get('client_secret'),
        tenant=SECRETS.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS.get('azure_cloud')))


@patch('chaosazure.ServicePrincipalCredentials', autospec=True)
def test_credential_using_flat_config_with_env(spcred):
    cred = MagicMock()
    spcred.return_value = cred

    os.putenv("SUBSCRIPTION_ID", "***REMOVED***")
    try:
        init_client(SECRETS, FLAT_CONFIG_FROM_EN)
    finally:
        os.environ.pop("SUBSCRIPTION_ID", None)

    spcred.assert_called_with(
        client_id=SECRETS.get("client_id"),
        secret=SECRETS.get('client_secret'),
        tenant=SECRETS.get('tenant_id'),
        cloud_environment=__get_cloud_env_by_name(SECRETS.get('azure_cloud')))
