# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""

from typing import List

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers import (
    PostgreSQLManagementClient as PostgreSQLFlexibleManagementClient
)
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from chaoslib.discovery import (discover_actions, discover_probes,
                                initialize_discovery_result)
from chaoslib.types import (Configuration, DiscoveredActivities, Discovery,
                            Secrets)
from logzero import logger

from chaosazure.auth import auth
from chaosazure.common.config import load_configuration, load_secrets


__all__ = [
    "discover", "__version__", "init_compute_management_client",
    "init_website_management_client", "init_resource_graph_client"
]
__version__ = '0.11.0'


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Azure capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-azure")

    discovery = initialize_discovery_result(
        "chaostoolkit-azure", __version__, "azure")
    discovery["activities"].extend(__load_exported_activities())
    return discovery


def init_compute_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> ComputeManagementClient:
    """
    Initializes Compute management client for virtual machine,
    and virtual machine scale sets resources under Azure Resource manager.
    """
    return __azure_client_factory("ComputeManagementClient", Secrets)


def init_postgresql_flexible_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> PostgreSQLFlexibleManagementClient:
    """
    Initializes Relational Database management client for postgresql_flexible,
    resources under Azure Resource manager.
    """
    return __azure_client_factory("PostgreSQLFlexibleManagementClient", Secrets)


def init_postgresql_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> PostgreSQLManagementClient:
    """
    Initializes Relational Database management client for postgresql,
    resources under Azure Resource manager.
    """
    return __azure_client_factory("PostgreSQLManagementClient", Secrets)


def init_website_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> WebSiteManagementClient:
    """
    Initializes Website management client for webapp resource under Azure
    Resource manager.
    """
    return __azure_client_factory("WebSiteManagementClient", Secrets)


def init_resource_graph_client(
        experiment_secrets: Secrets) -> ResourceGraphClient:
    """
    Initializes Resource Graph client.
    """
    return __azure_client_factory("ResourceGraphClient", Secrets)


def init_redis_client(
        experiment_secrets: Secrets) -> ResourceGraphClient:
    """
    Initializes Resource Graph client.
    """
    return __azure_client_factory("RedisManagementClient", Secrets)


def init_eventhub_client(
        experiment_secrets: Secrets) -> ResourceGraphClient:
    """
    Initializes Resource Graph client.
    """
    return __azure_client_factory("EventHubManagementClient", Secrets)


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
    activities.extend(discover_actions("chaosazure.postgresql_flexible.actions"))
    activities.extend(discover_probes("chaosazure.postgresql_flexible.probes"))
    activities.extend(discover_actions("chaosazure.postgresql.actions"))
    activities.extend(discover_probes("chaosazure.postgresql.probes"))
    activities.extend(discover_actions("chaosazure.redis.actions"))
    activities.extend(discover_probes("chaosazure.redis.probes"))
    activities.extend(discover_actions("chaosazure.eventhub.actions"))
    activities.extend(discover_probes("chaosazure.eventhub.probes"))
    return activities


def __azure_client_factory(experiment_secrets: Secrets, client_name: str) -> object:
    """
    Simple factory for *Clients in azure.mgmt
    """
    secrets = load_secrets(experiment_secrets)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = eval(client_name)(
            credential=authentication,
            credential_scopes=scopes,
            base_url=base_url)

        return client
