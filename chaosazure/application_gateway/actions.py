# -*- coding: utf-8 -*-
import re

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_network_management_client
from chaosazure.common import cleanse
from chaosazure.application_gateway.constants import RES_TYPE_SRV_AG
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["delete_application_gateways", "start_application_gateways",
           "stop_application_gateways", "delete_routes"]

from chaosazure.vmss.records import Records


def delete_application_gateways(filter: str = None,
                                configuration: Configuration = None,
                                secrets: Secrets = None):
    """
    Delete application gateways at random.

    **Be aware**: Deleting an application gateway is an invasive action. You will not be
    able to recover the application gateway once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the application gateways. If the filter is omitted all application gateways in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_application_gateways("where resourceGroup=='rg'", c, s)
    Delete all application_gateways from the group 'rg'

    >>> delete_application_gateways("where resourceGroup=='rg' and name='name'", c, s)
    Delete the application gateway from the group 'rg' having the name 'name'

    >>> delete_application_gateways("where resourceGroup=='rg' | sample 2", c, s)
    Delete two application_gateways at random from the group 'rg'
    """
    logger.debug(
        "Start delete_application_gateways: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    application_gateways = __fetch_application_gateways(filter, configuration, secrets)
    client = __network_mgmt_client(secrets, configuration)
    application_gateway_records = Records()
    for agw in application_gateways:
        group = agw['resourceGroup']
        name = agw['name']
        logger.debug("Deleting application gateway: {}".format(name))
        client.application_gateways.begin_delete(group, name)
        application_gateway_records.add(cleanse.application_gateway(agw))

    return application_gateway_records.output_as_dict('resources')


def start_application_gateways(filter: str = None,
                               configuration: Configuration = None,
                               secrets: Secrets = None):
    """
    Start application gateway at random.

    Parameters
    ----------
    filter : str, optional
        Filter the application gateway. If the filter is omitted all application gateway in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> start_application_gateways("where resourceGroup=='rg'", c, s)
    Start all application gateways from the group 'rg'

    >>> start_application_gateways("where resourceGroup=='rg' and name='name'", c, s)
    Start the application gateway from the group 'rg' having the name 'name'

    >>> start_application_gateways("where resourceGroup=='rg' | sample 2", c, s)
    Start two application gateways at random from the group 'rg'
    """
    logger.debug(
        "Start start_application_gateways: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    application_gateways = __fetch_application_gateways(filter, configuration, secrets)
    client = __network_mgmt_client(secrets, configuration)
    application_gateway_records = Records()
    for agw in application_gateways:
        group = agw['resourceGroup']
        name = agw['name']
        logger.debug("Starting application gateway: {}".format(name))
        client.application_gateways.begin_start(group, name)
        application_gateway_records.add(cleanse.application_gateway(agw))

    return application_gateway_records.output_as_dict('resources')


def stop_application_gateways(filter: str = None,
                              configuration: Configuration = None,
                              secrets: Secrets = None):
    """
    Stop application gateways at random.

    Parameters
    ----------
    filter : str, optional
        Filter the application gateways. If the filter is omitted all application gateways
        in the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stop_application_gateways("where resourceGroup=='rg'", c, s)
    Stop all application gateways from the group 'rg'

    >>> stop_application_gateways("where resourceGroup=='rg' and name='name'", c, s)
    Stop the application gateway from the group 'rg' having the name 'name'

    >>> stop_application_gateways("where resourceGroup=='rg' | sample 2", c, s)
    Stop two application gateways at random from the group 'rg'
    """
    logger.debug(
        "Start stop_application_gateways: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    application_gateways = __fetch_application_gateways(filter, configuration, secrets)
    client = __network_mgmt_client(secrets, configuration)
    application_gateway_records = Records()
    for agw in application_gateways:
        group = agw['resourceGroup']
        name = agw['name']
        logger.debug("Stopping application gateway: {}".format(name))
        client.application_gateways.begin_stop(group, name)
        application_gateway_records.add(cleanse.application_gateway(agw))

    return application_gateway_records.output_as_dict('resources')


def delete_routes(filter: str = None,
                  name_pattern: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Delete routes at random.
    **Be aware**: Deleting a route is an invasive action. You will not be
    able to recover the route once you deleted it.
    Parameters
    ----------
    filter : str, optional
        Filter the application gateways. If the filter is omitted all routes
        of all application gateways in the subscription will be selected
        as potential chaos candidates.
    name_pattern : str, optional
        Filter the routes. If the filter is omitted all routes except the first in
        the server will be selected for the probe.
        Pattern example:
        'app[0-9]{3}'
    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/
    >>> delete_routes("where resourceGroup=='rg'", 'chaos-*', c, s)
    Delete all route named 'chaos-*' in all application gateways from the group 'rg'
    >>> delete_routes("where resourceGroup=='rg' and name='name'", 'chaos-test', c, s)
    Delete all route named 'chaos-*' the server from the group 'rg' having the name 'name'

    If all routes are deleted the first will be kept
    """
    logger.debug(
        "Start delete_routes: "
        "configuration='{}', filter='{}', name_pattern='{}'".format(
            configuration, filter, name_pattern))

    pattern = None
    if name_pattern:
        pattern = re.compile(name_pattern)

    application_gateways = __fetch_application_gateways(filter, configuration, secrets)
    client = __network_mgmt_client(secrets, configuration)
    route_records = Records()
    for agw in application_gateways:
        group = agw['resourceGroup']
        application_gateway_name = agw['name']
        app_gw = client.application_gateways.get(group, application_gateway_name)
        route_to_keep = app_gw.request_routing_rules[0]

        for r in app_gw.request_routing_rules[:]:
            name = r.name
            if pattern is None or pattern.search(name):
                app_gw.request_routing_rules.remove(r)
                route_records.add(r.as_dict())
                logger.debug("Deleting route: {}/{}".format(application_gateway_name, name))

        if not app_gw.request_routing_rules:
            app_gw.request_routing_rules.append(route_to_keep)
            logger.debug("Routes cannot be empty added back: {}/{}".format(application_gateway_name,
                                                                           route_to_keep.name))

        client.application_gateways.begin_create_or_update(group, application_gateway_name, app_gw)

    return route_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################


def __fetch_application_gateways(filter, configuration, secrets) -> []:
    application_gateways = fetch_resources(filter, RES_TYPE_SRV_AG, secrets, configuration)
    if not application_gateways:
        logger.warning("No application gateways found")
        raise FailedActivity("No application gateways found")
    else:
        logger.debug(
            "Fetched application gateways: {}".format(
                [s['name'] for s in application_gateways]))
    return application_gateways


def __network_mgmt_client(secrets, configuration):
    return init_network_management_client(secrets, configuration)
