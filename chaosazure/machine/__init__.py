# -*- coding: utf-8 -*-
import contextlib
import os.path

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from msrestazure.azure_active_directory import ServicePrincipalCredentials

__all__ = ["auth"]


@contextlib.contextmanager
def auth(configuration: Configuration, secrets: Secrets) -> ServicePrincipalCredentials:
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
            "subscription_id": "your-azure-subscription-id",
            "resource_groups": "resourceGroup1,resourceGroup2,..."
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

    The client_id, tenant_id, and client_secret content will be read
    from the specified local environment variables, e.g. `AZURE_CLIENT_ID`,
    `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET` that you will have populated
    before hand.
    ```

    Using this function goes as follows:

    ```python
    with auth(configuration, secrets) as cred:
        azure_subscription_id = configuration['azure']['subscription_id']
        resource_client = ResourceManagementClient(cred, azure_subscription_id)
        compute_client = ComputeManagementClient(cred, azure_subscription_id)
    ```
    """
    c = configuration or {}
    s = secrets or {}

    azure_config = c.get("azure")
    azure_secrets = s.get("azure")

    if not azure_config:
        raise FailedActivity("Azure configuration not found")

    if not azure_secrets:
        raise FailedActivity("Azure secrets not found")

    #
    # fetch secrets from environment
    #
    client_id = os.getenv(azure_secrets.get('client_id'))
    client_secret = os.getenv(azure_secrets.get('client_secret'))
    tenant_id = os.getenv(azure_secrets.get('tenant_id'))

    if not client_id or not client_secret or not tenant_id:
        raise FailedActivity("Client could not find Azure credentials")

    #
    # build service principal credential object
    #
    credentials = ServicePrincipalCredentials(
        client_id=client_id,
        secret=client_secret,
        tenant=tenant_id
    )

    yield credentials
