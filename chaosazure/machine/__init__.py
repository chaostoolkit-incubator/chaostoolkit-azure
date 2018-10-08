# -*- coding: utf-8 -*-
import contextlib
import os.path

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Secrets
from msrestazure.azure_active_directory import ServicePrincipalCredentials

__all__ = ["auth"]


@contextlib.contextmanager
def auth(secrets: Secrets) -> ServicePrincipalCredentials:
    """
    Attempt to load the Azure authentication information from a local
    configuration file or the passed `configuration` mapping. The latter takes
    precedence over the local configuration file.

    If you provide a secrets dictionary, the returned mapping will
    be created from their content. For instance, you could have:

    Secrets mapping (in your experiment file):
    ```json
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
    with auth(secrets) as cred:
        azure_subscription_id = configuration['azure']['subscription_id']
        resource_client = ResourceManagementClient(cred, azure_subscription_id)
        compute_client = ComputeManagementClient(cred, azure_subscription_id)
    ```
    """
    azure_secrets = secrets or {}

    if not azure_secrets:
        raise FailedActivity("Azure secrets not found")

    client_id, client_secret, tenant_id = __fetch_secrets(azure_secrets)
    __check_secrets(client_id, client_secret, tenant_id)
    credentials = __generate_service_principal_credentials(client_id, client_secret, tenant_id)

    yield credentials


def __generate_service_principal_credentials(client_id, client_secret, tenant_id):
    credentials = ServicePrincipalCredentials(
        client_id=client_id,
        secret=client_secret,
        tenant=tenant_id
    )
    return credentials


def __check_secrets(client_id, client_secret, tenant_id):
    if not client_id or not client_secret or not tenant_id:
        raise FailedActivity("Client could not find Azure credentials")


def __fetch_secrets(azure_secrets):
    #
    # fetch secrets from environment
    #
    client_id = os.getenv(azure_secrets.get('client_id'))
    client_secret = os.getenv(azure_secrets.get('client_secret'))
    tenant_id = os.getenv(azure_secrets.get('tenant_id'))

    #
    # fetch secrets from file content itself when empty
    #
    if not client_id:
        client_id = azure_secrets.get('client_id')
    if not client_secret:
        client_secret = azure_secrets.get('client_secret')
    if not tenant_id:
        tenant_id = azure_secrets.get('tenant_id')
    return client_id, client_secret, tenant_id
