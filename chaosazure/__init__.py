# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""
import contextlib
from chaoslib.discovery import initialize_discovery_result, discover_actions, \
    discover_probes
from chaoslib.types import Discovery, DiscoveredActivities, Secrets
from logzero import logger
from msrestazure.azure_active_directory import ServicePrincipalCredentials
from typing import List

__all__ = ["auth", "discover", "__version__"]
__version__ = '0.5.0'


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
    creds = dict(
        azure_client_id=None, azure_client_secret=None, azure_tenant_id=None)

    if secrets:
        creds["azure_client_id"] = secrets.get("client_id")
        creds["azure_client_secret"] = secrets.get("client_secret")
        creds["azure_tenant_id"] = secrets.get("tenant_id")

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


###############################################################################
# Private functions
###############################################################################
def __get_credentials(creds):
    credentials = ServicePrincipalCredentials(
        client_id=creds['azure_client_id'],
        secret=creds['azure_client_secret'],
        tenant=creds['azure_tenant_id']
    )
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
