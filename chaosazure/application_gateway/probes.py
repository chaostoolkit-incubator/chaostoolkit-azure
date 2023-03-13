# -*- coding: utf-8 -*-
import re

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.application_gateway.constants import RES_TYPE_SRV_AG
from chaosazure.application_gateway.actions import __network_mgmt_client
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_application_gateways", "count_application_gateways", "describe_routes"]


def describe_application_gateways(filter: str = None,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None):
    """
    Describe Azure application gateways.

    Parameters
    ----------
    filter : str
        Filter the application gateways. If the filter is omitted all application gateways in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start describe_application_gateways: configuration='{}', filter='{}'".format(
            configuration, filter))

    application_gateways = fetch_resources(filter, RES_TYPE_SRV_AG, secrets, configuration)
    return application_gateways


def count_application_gateways(filter: str = None,
                               configuration: Configuration = None,
                               secrets: Secrets = None) -> int:
    """
    Return count of Azure application gateways.

    Parameters
    ----------
    filter : str
        Filter the application gateways. If the filter is omitted all application_gateways in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start count_application_gateways: configuration='{}', filter='{}'".format(
            configuration, filter))

    application_gateways = fetch_resources(filter, RES_TYPE_SRV_AG, secrets, configuration)
    return len(application_gateways)


def describe_routes(filter: str = None,
                    name_pattern: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Describe Azure application gateways routes.

    Parameters
    ----------
    filter : str
        Filter the application_gateways. If the filter is omitted all application gateways in
        the subscription will be selected for the probe.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    name_pattern : str
        Filter the routes. If the filter is omitted all routes in
        the server will be selected for the probe.
        Pattern example:
        'app[0-9]{3}'
    """
    logger.debug(
        "Start describe_routes: configuration='{}', filter='{}', name_pattern='{}'".format(
            configuration, filter, name_pattern))

    pattern = None
    if name_pattern:
        pattern = re.compile(name_pattern)

    application_gateways = fetch_resources(filter, RES_TYPE_SRV_AG, secrets, configuration)
    client = __network_mgmt_client(secrets, configuration)
    routes = []
    for agw in application_gateways:
        group = agw['resourceGroup']
        application_gateway_name = agw['name']
        app_gw = client.application_gateways.get(group, application_gateway_name)

        for r in app_gw.request_routing_rules:
            name = r.name
            if pattern is None or pattern.search(name):
                routes.append(r.as_dict())

    return routes
