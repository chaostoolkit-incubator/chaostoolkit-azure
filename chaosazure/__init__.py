# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""
import contextlib
from typing import List

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from chaoslib.discovery import initialize_discovery_result, \
    discover_actions, discover_probes
from chaoslib.types import Discovery, DiscoveredActivities, \
    Secrets, Configuration
from logzero import logger
from msrestazure.azure_active_directory import AADMixin

from chaosazure.auth import Auth, create

__all__ = [
    "auth", "discover", "__version__", "init_client",
    "init_resource_graph_client"
]
__version__ = '0.7.0'

from chaosazure.common import cloud


@contextlib.contextmanager
def auth(secrets: Secrets) -> AADMixin:
    """
    Attempt to load the Azure authentication information from a local
    configuration file or the passed `configuration` mapping. The latter takes
    precedence over the local configuration file. Service principle and token
    based credentials are supported. Token based credentials do not currently
    support refresh token functionality.

    If you provide a secrets dictionary, the returned mapping will
    be created from their content. For example, a service principle based
    credential has:

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
    you can feed the cloud environment name. If omitted the Public Cloud is
    taken as default.
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
        azure_subscription_id = configuration.get("azure_subscription_id")
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

    # No input validation needed:
    # 1) Either no secrets are passed at all - chaostoolkit-lib
    #    will handle it for us *or*
    # 2) Secret arguments are partially missing or invalid - we
    #    rely on the ms azure library
    yield create(secrets)


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Azure capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-azure")

    discovery = initialize_discovery_result(
        "chaostoolkit-azure", __version__, "azure")
    discovery["activities"].extend(__load_exported_activities())
    return discovery


def init_client(
        secrets: Secrets,
        configuration: Configuration) -> ComputeManagementClient:
    with auth(secrets) as authentication:
        _subscription_id = configuration.get("azure_subscription_id")
        if not _subscription_id:
            _subscription_id = configuration['azure']['subscription_id']
        _base_url = authentication.cloud_environment.endpoints.resource_manager

        client = ComputeManagementClient(
            credentials=authentication,
            subscription_id=_subscription_id,
            base_url=_base_url)

        return client


def init_resource_graph_client(secrets: Secrets) -> ResourceGraphClient:
    with auth(secrets) as authentication:
        _base_url = authentication.cloud_environment.endpoints.resource_manager

        client = ResourceGraphClient(
            credentials=authentication,
            base_url=_base_url)

        return client


###############################################################################
# Private functions
###############################################################################
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
