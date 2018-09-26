# -*- coding: utf-8 -*-
import contextlib
import os.path

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets

__all__ = ["auth"]


@contextlib.contextmanager
def auth(configuration: Configuration, secrets: Secrets):
    """
    Attempt to load the Azure authentication information from a local
    configuration file or the passed `configuration` mapping. The latter takes
    precedence over the local configuration file.

    If you provide a configuration and secrets dictionary, the returned mapping
    will be created from their content. For instance, you could have:

    Configuration mapping (in your experiment file):
    ```python
    {
        "azure": {
            "subscription_id": "AZURE_SUBSCRIPTION_ID",
            "resource_groups": "resourceGroup1,resourceGroup2"
        }
    }
    ```

    Secrets mapping (in your experiment file):
    ```python
    {
        "azure": {
            "client_id": "AZURE_CLIENT_ID",
            "client_secret": "AZURE_CLIENT_SECRET",
            "tenant_id": "AZURE_TENANT_ID"
        }
    }
    ```

    The client_id, tenant_id, client_secret and tenant_id content will be
    read from the local environment variables `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`,
    `AZURE_CLIENT_SECRET`, and `AZURE_TENANT_ID` that you will have populated before
    hand. The content will be saved by the extension into a temporary file
    before being used to authenticate.
    ```

    Using this function goes as follows:

    ```python
    with auth(configuration, secrets) as info:
        url = "{}{}".format(
            info["endpoint"], "/Tools/Chaos/$/Start?api-version=6.0")

        r = requests.get(
            url, cert=info["security"]["path"], verify=info["verify"])

    """
    c = configuration or {}
    s = secrets or {}

    azure_config = c.get("azure")
    azure_secrets = s.get("azure")

    if not azure_config:
        raise FailedActivity("Azure configuration not found")

    if not azure_secrets:
        raise FailedActivity("Azure secrets not found")

    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    client_id = os.environ['AZURE_CLIENT_ID']
    secret = os.environ['AZURE_CLIENT_SECRET']
    tenant = os.environ['AZURE_TENANT_ID']

    if not subscription_id or not client_id or not secret or not tenant:
        raise FailedActivity("Client could not find Azure credentials")

    info = {
        "subscription_id": subscription_id,
        "resource_groups": azure_config.get("resource_groups"),
        "security": {
            "client_id": client_id,
            "client_secret": secret,
            "tenant_id": tenant
        }
    }

    yield info
