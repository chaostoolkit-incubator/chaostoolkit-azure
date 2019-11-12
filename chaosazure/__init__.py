# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""
import contextlib
from typing import List

from adal import AuthenticationContext
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from chaoslib.discovery import initialize_discovery_result, discover_actions, \
    discover_probes
from chaoslib.types import Discovery, DiscoveredActivities, \
    Secrets, Configuration
from logzero import logger
import msrestazure
from msrestazure.azure_active_directory import ServicePrincipalCredentials, \
    AADTokenCredentials
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD, \
    AZURE_US_GOV_CLOUD, AZURE_GERMAN_CLOUD, AZURE_CHINA_CLOUD

__all__ = ["auth", "discover", "__version__", "init_client",
           "init_resource_graph_client"]
__version__ = '0.6.0'


@contextlib.contextmanager
def auth(secrets: Secrets) -> ServicePrincipalCredentials:
    """
    Attempt to load the Azure authentication information from a local
    configuration file or the passed `configuration` mapping. The latter takes
    precedence over the local configuration file. Service principle and token
    based credentials are supported. Token based credentials do not currently
    support refresh token functionality.

    If you provide a secrets dictionary, the returned mapping will
    be created from their content. For instance, for service principle based
    credentials, you could have:

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
    Also if you are not working with Public Global Azure, e.g. China Cloud
    You can feed the cloud environment name as well.
    Please refer to msrestazure.azure_cloud
    ```json
    {
        "azure": {
            "client_id": "xxxxxxx",
            "client_secret": "*******",
            "tenant_id": "@@@@@@@@@@@",
            "azure_cloud": "AZURE_CHINA_CLOUD"
        }
    }
    ```

    The client_id, tenant_id, and client_secret content will be read
    from the specified local environment variables, e.g. `AZURE_CLIENT_ID`,
    `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET` that you will have populated
    before hand.

    If the client_secret is not provided, then token based credentials is
    assumed and an access_token value must be present and updated as the token
    expires.
    ```

    Using this function goes as follows:

    ```python
    with auth(secrets) as cred:
        azure_subscription_id = configuration['azure']['subscription_id']
        resource_client = ResourceManagementClient(cred, azure_subscription_id)
        compute_client = ComputeManagementClient(cred, azure_subscription_id)
    ```

    Again, if you are not working with Public Azure Cloud,
    and you set azure_cloud in secret,
    this will pass one more parameter `base_url` to above function.
    ```python
        cloud = __get_cloud_env_by_name(creds['azure_cloud'])
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id,
                        base_url=cloud.endpoints.resource_manager)
    ```

    """
    creds = dict(
        azure_client_id=None, azure_client_secret=None,
        azure_tenant_id=None, azure_cloud=None)

    if secrets:
        creds["azure_client_id"] = secrets.get("client_id")
        creds["azure_client_secret"] = secrets.get("client_secret")
        creds["azure_tenant_id"] = secrets.get("tenant_id")
        creds["azure_cloud"] = secrets.get("azure_cloud", "AZURE_PUBLIC_CLOUD")
        creds["access_token"] = secrets.get("access_token")

    credentials = __get_credentials(creds)

    yield credentials


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Azure capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-azure")

    discovery = initialize_discovery_result(
        "chaostoolkit-azure", __version__, "azure")
    discovery["activities"].extend(__load_exported_activities())
    return discovery


def init_client(secrets: Secrets, configuration: Configuration) \
        -> ComputeManagementClient:
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        base_url = __get_cloud_env_by_name(
            secrets.get("azure_cloud")).endpoints.resource_manager
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id,
            base_url=base_url)

        return client


def init_resource_graph_client(secrets: Secrets) -> ResourceGraphClient:
    with auth(secrets) as cred:
        base_url = __get_cloud_env_by_name(
            secrets.get("azure_cloud")).endpoints.resource_manager
        client = ResourceGraphClient(
            credentials=cred,
            base_url=base_url)

        return client


###############################################################################
# Private functions
###############################################################################
def __get_credentials(creds: dict) -> ServicePrincipalCredentials:
    if creds['azure_client_secret'] is not None:
        credentials = ServicePrincipalCredentials(
            client_id=creds['azure_client_id'],
            secret=creds['azure_client_secret'],
            tenant=creds['azure_tenant_id'],
            cloud_environment=__get_cloud_env_by_name(creds['azure_cloud'])
        )
    else:
        token = dict(accessToken=creds['access_token'])
        credentials = AADTokenCredentials(token, creds['azure_client_id'])
    return credentials


def __load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosazure.machine.actions"))
    activities.extend(discover_probes("chaosazure.machine.probes"))
    activities.extend(discover_actions("chaosazure.aks.actions"))
    activities.extend(discover_actions("chaosazure.vmss.actions"))
    activities.extend(discover_actions("chaosazure.webapp.actions"))
    activities.extend(discover_probes("chaosazure.webapp.probes"))
    return activities


def __get_cloud_env_by_name(cloud: str = None) \
        -> msrestazure.azure_cloud.Cloud:
    try:
        if cloud is None:
            return msrestazure.azure_cloud.AZURE_PUBLIC_CLOUD

        cloud = cloud.strip()
        if cloud == "AZURE_CHINA_CLOUD":
            return msrestazure.azure_cloud.AZURE_CHINA_CLOUD
        elif cloud == "AZURE_US_GOV_CLOUD":
            return msrestazure.azure_cloud.AZURE_US_GOV_CLOUD
        elif cloud == "AZURE_GERMAN_CLOUD":
            return msrestazure.azure_cloud.AZURE_GERMAN_CLOUD
        else:
            return msrestazure.azure_cloud.AZURE_PUBLIC_CLOUD
    except AttributeError:
        logger.info("Invalid azure cloud name, use default AZURE_PUBLIC_CLOUD")
        return msrestazure.azure_cloud.AZURE_PUBLIC_CLOUD
