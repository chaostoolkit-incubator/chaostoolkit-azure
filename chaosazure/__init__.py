# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""

from typing import List

from azure.mgmt.compute import ComputeManagementClient
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
__version__ = '0.9.0'


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
        client = ComputeManagementClient(
            credentials=authentication,
            subscription_id=configuration.get('subscription_id'),
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
        client = WebSiteManagementClient(
            credentials=authentication,
            subscription_id=configuration.get('subscription_id'),
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
        client = ResourceGraphClient(
            credential=authentication,
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
    activities.extend(discover_actions("chaosazure.vmss.actions"))
    activities.extend(discover_actions("chaosazure.webapp.actions"))
    activities.extend(discover_probes("chaosazure.webapp.probes"))
    return activities
