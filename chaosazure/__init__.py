# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""
import os
from typing import List

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.rdbms.postgresql_flexibleservers import (
    PostgreSQLManagementClient as PostgreSQLFlexibleManagementClient
)
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.netapp import NetAppManagementClient
from azure.mgmt.storage import StorageManagementClient
from chaoslib.discovery import (discover_actions, discover_probes,
                                initialize_discovery_result)
from chaoslib.types import (Configuration, DiscoveredActivities, Discovery,
                            Secrets)
from logzero import logger

from chaosazure.auth import auth
from chaosazure.common.config import load_configuration, load_secrets


__all__ = [
    "discover", "__version__", "init_compute_management_client", "init_network_management_client",
    "init_website_management_client", "init_resource_graph_client", "init_netapp_management_client",
    "init_storage_management_client"
]
__version__ = '0.15.2'


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
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = ComputeManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_containerservice_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> ContainerServiceClient:
    """
    Initializes Container Service management client for managed clusters
    resources under Azure Resource manager.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = ContainerServiceClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_postgresql_flexible_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> PostgreSQLFlexibleManagementClient:
    """
    Initializes Relational Database management client for postgresql_flexible,
    resources under Azure Resource manager.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = PostgreSQLFlexibleManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_postgresql_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> PostgreSQLManagementClient:
    """
    Initializes Relational Database management client for postgresql,
    resources under Azure Resource manager.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = PostgreSQLManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_network_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> NetworkManagementClient:
    """
    Initializes Network management client for application gateway,
    resources under Azure Resource manager.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = NetworkManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_website_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> WebSiteManagementClient:
    """
    Initializes Website management client for webapp resource under Azure
    Resource manager.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = WebSiteManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_resource_graph_client(
        experiment_secrets: Secrets) -> ResourceGraphClient:
    """
    Initializes Resource Graph client.
    """
    secrets = load_secrets(experiment_secrets)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = ResourceGraphClient(
            credential=authentication,
            credential_scopes=scopes,
            base_url=base_url)

        return client


def init_netapp_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> NetAppManagementClient:
    """
    Initializes NetApp management client.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = NetAppManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

        return client


def init_storage_management_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> StorageManagementClient:
    """
    Initializes Storage management client.
    """
    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        scopes = [base_url + "/.default"]
        client = StorageManagementClient(
            credential=authentication,
            credential_scopes=scopes,
            subscription_id=configuration.get(
                'subscription_id', os.getenv("AZURE_SUBSCRIPTION_ID")),
            base_url=base_url)

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
    activities.extend(discover_probes("chaosazure.aks.probes"))
    activities.extend(discover_actions("chaosazure.vmss.actions"))
    activities.extend(discover_actions("chaosazure.webapp.actions"))
    activities.extend(discover_probes("chaosazure.webapp.probes"))
    activities.extend(discover_actions("chaosazure.postgresql_flexible.actions"))
    activities.extend(discover_probes("chaosazure.postgresql_flexible.probes"))
    activities.extend(discover_actions("chaosazure.application_gateway.actions"))
    activities.extend(discover_probes("chaosazure.application_gateway.probes"))
    activities.extend(discover_actions("chaosazure.postgresql.actions"))
    activities.extend(discover_probes("chaosazure.postgresql.probes"))
    activities.extend(discover_actions("chaosazure.netapp.actions"))
    activities.extend(discover_probes("chaosazure.netapp.probes"))
    activities.extend(discover_actions("chaosazure.storage.actions"))
    activities.extend(discover_probes("chaosazure.storage.probes"))
    return activities
