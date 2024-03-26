import contextlib
import os
from typing import Dict, Generator

from azure.identity import DefaultAzureCredential
from azure.identity._constants import AzureAuthorityHosts


@contextlib.contextmanager
def auth(secrets: Dict) -> Generator[DefaultAzureCredential, None, None]:
    """
    Create Azure authentication client from a provided secrets using
    the `https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python`
    class.

    For example, secrets that contains a `client_id`, `client_secret` and
    `tenant_id`:
    ```python
    {
        "client_id": "AZURE_CLIENT_ID",
        "client_secret": "AZURE_CLIENT_SECRET",
        "tenant_id": "AZURE_TENANT_ID"
    }
    ```
    If you are not working with Public Global Azure, e.g. China Cloud
    you can provide `"AZURE_CHINA"` string. If omitted the
    Public Cloud is taken as default.
    ```python
    {
        "client_id": "xxxxxxx",
        "client_secret": "*******",
        "tenant_id": "@@@@@@@@@@@",
        "cloud": "AZURE_CHINA"
    }
    ```

    You can also omit any configuration or secrets and let Azure cycle through
    all the potential client candidates.

    Using this function goes as follows:

    ```python
    with auth(secrets) as cred:
        subscription_id = configuration.get("subscription_id")
        resource_client = ResourceManagementClient(cred, subscription_id)
        compute_client = ComputeManagementClient(cred, subscription_id)
    ```

    Again, if you are not working with Public Azure Cloud,
    and you set azure_cloud in secret,
    this will pass one more parameter `base_url` to above function.
    ```python
    with auth(secrets) as cred:
        cloud = cred.get('cloud')
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id,
                        base_url=cloud.endpoints.resource_manager)
    ```

    """
    yield make_auth(secrets)


def make_auth(secrets: Dict) -> DefaultAzureCredential:
    if os.getenv("AZURE_CLIENT_ID") is None:
        os.putenv("AZURE_CLIENT_ID", secrets.get("client_id", ""))

    if os.getenv("AZURE_CLIENT_SECRET") is None:
        os.putenv("AZURE_CLIENT_SECRET", secrets.get("client_secret", ""))

    if os.getenv("AZURE_TENANT_ID") is None:
        os.putenv("AZURE_TENANT_ID", secrets.get("tenant_id", ""))

    authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD

    if os.getenv("AZURE_AUTHORITY_HOST") is None:
        cloud_authority = secrets.get(
            "cloud", os.getenv("AZURE_CLOUD", "AZURE_PUBLIC_CLOUD")
        )

        if cloud_authority == "AZURE_PUBLIC_CLOUD":
            authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD
        elif cloud_authority == "AZURE_GERMAN_CLOUD":
            authority = AzureAuthorityHosts.AZURE_GERMANY
        elif cloud_authority == "AZURE_US_GOV_CLOUD":
            authority = AzureAuthorityHosts.AZURE_GOVERNMENT
        elif cloud_authority == "AZURE_CHINA_CLOUD":
            authority = AzureAuthorityHosts.AZURE_CHINA

    return DefaultAzureCredential(authority=authority)
