from chaoslib import Configuration, Secrets
from logzero import logger

from chaosazure.rgraph.resource_graph import fetch_resources
from chaosazure.webapp.constants import RES_TYPE_WEBAPP


def describe_webapps(filter: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Describe Azure web apps.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start describe_webapps: configuration='{}', filter='{}'".format(
            configuration, filter))

    webapps = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)
    return webapps


def count_webapps(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> int:
    """
    Return count of Azure web apps.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start count_machines: configuration='{}', filter='{}'".format(
            configuration, filter))

    webapps = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)
    return len(webapps)
