# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""
from typing import List

from chaoslib.discovery import initialize_discovery_result, discover_actions, \
    discover_probes
from chaoslib.types import Discovery, DiscoveredActivities
from logzero import logger

__all__ = ["discover", "__version__"]
__version__ = '0.1.3'


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
def __load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosazure.fabric.actions"))
    activities.extend(discover_probes("chaosazure.fabric.probes"))
    activities.extend(discover_actions("chaosazure.machine.actions"))
    activities.extend(discover_probes("chaosazure.machine.probes"))
    return activities
