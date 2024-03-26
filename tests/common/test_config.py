import os

from chaosazure import get_management_url_from_authority
from chaosazure.common import config

settings_dir = os.path.join(os.path.dirname(__file__), "fixtures")


def test_load_secrets_from_experiment_dict():
    # arrange
    experiment_secrets = {
        "client_id": "AZURE_CLIENT_ID",
        "client_secret": "AZURE_CLIENT_SECRET",
        "tenant_id": "AZURE_TENANT_ID",
    }

    # act
    secrets = config.load_secrets(experiment_secrets)

    # assert
    assert secrets.get("client_id") == "AZURE_CLIENT_ID"
    assert secrets.get("client_secret") == "AZURE_CLIENT_SECRET"
    assert secrets.get("tenant_id") == "AZURE_TENANT_ID"
    assert (
        get_management_url_from_authority(secrets)
        == "https://management.azure.com"
    )


def test_load_token_from_experiment_dict():
    # arrange
    experiment_secrets = {"access_token": "ACCESS_TOKEN"}

    # act
    secrets = config.load_secrets(experiment_secrets)

    # assert
    assert secrets.get("access_token") == "ACCESS_TOKEN"
    assert (
        get_management_url_from_authority(secrets)
        == "https://management.azure.com"
    )


def test_load_subscription_from_experiment_dict():
    # arrange
    experiment_configuration = {
        "azure_subscription_id": "AZURE_SUBSCRIPTION_ID",
        "some_other_settings": "OTHER_SETTING",
    }

    # act
    configuration = config.load_configuration(experiment_configuration)

    # assert
    assert configuration.get("subscription_id") == "AZURE_SUBSCRIPTION_ID"


def test_load_legacy_subscription_from_experiment_dict():
    # arrange
    experiment_configuration = {
        "azure": {"subscription_id": "AZURE_SUBSCRIPTION_ID"}
    }

    # act
    configuration = config.load_configuration(experiment_configuration)

    # assert
    assert configuration.get("subscription_id") == "AZURE_SUBSCRIPTION_ID"


def test_load_subscription_from_credential_file(monkeypatch):
    # arrange
    experiment_configuration = None
    monkeypatch.setenv(
        "AZURE_AUTH_LOCATION", os.path.join(settings_dir, "credentials.json")
    )

    # act
    configuration = config.load_configuration(experiment_configuration)

    # assert
    assert configuration.get("subscription_id") == "AZURE_SUBSCRIPTION_ID"
