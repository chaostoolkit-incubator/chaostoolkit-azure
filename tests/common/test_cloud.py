import pytest
from chaoslib.exceptions import InterruptExecution
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD, \
    AZURE_US_GOV_CLOUD, AZURE_GERMAN_CLOUD, AZURE_CHINA_CLOUD

from chaosazure.common import cloud
from tests.data import secrets_provider

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


def test_resolve_cloud_env_by_name_default():
    data = secrets_provider.provide_secrets_via_service_principal()
    result = cloud.get_or_raise(data.get("azure_cloud")) \
        .endpoints.resource_manager

    assert result == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


def test_get_env_by_name_china():
    data = secrets_provider.provide_secrets_china()
    result = cloud.get_or_raise(data.get("azure_cloud")) \
        .endpoints.resource_manager

    assert result == AZURE_CHINA_CLOUD.endpoints.resource_manager


def test_get_env_by_name_public():
    data = secrets_provider.provide_secrets_public()
    result = cloud.get_or_raise(data.get("azure_cloud")) \
        .endpoints.resource_manager

    assert result == AZURE_PUBLIC_CLOUD.endpoints.resource_manager


def test_get_env_by_name_germany():
    data = secrets_provider.provide_secrets_germany()
    result = cloud.get_or_raise(data.get("azure_cloud")) \
        .endpoints.resource_manager

    assert result == AZURE_GERMAN_CLOUD.endpoints.resource_manager


def test_get_env_by_name_usgov():
    data = secrets_provider.provide_secrets_us_gov()
    result = cloud.get_or_raise(data.get("azure_cloud")) \
        .endpoints.resource_manager

    assert result == AZURE_US_GOV_CLOUD.endpoints.resource_manager


def test_get_env_by_name_bad():
    with pytest.raises(InterruptExecution):
        data = secrets_provider.provide_secrets_invalid_cloud()
        cloud.get_or_raise(data.get("azure_cloud")) \
            .endpoints.resource_manager
