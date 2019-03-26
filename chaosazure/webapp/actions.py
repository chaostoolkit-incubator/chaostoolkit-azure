import random
from azure.mgmt.web import WebSiteManagementClient
from chaoslib import Secrets, Configuration
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import auth
from chaosazure.rgraph.resource_graph import fetch_resources
from chaosazure.webapp.constants import RES_TYPE_WEBAPP

__all__ = ["stop_webapp", "restart_webapp", "start_webapp", "delete_webapp"]


def stop_webapp(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Stop a web app at random.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start stop_webapp: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_webapp_at_random(filter, configuration, secrets)

    logger.debug("Stopping web app: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.web_apps.stop(choice['resourceGroup'], choice['name'])


def restart_webapp(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Restart a web app at random.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start restart_webapp: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_webapp_at_random(filter, configuration, secrets)

    logger.debug("Restarting web app: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.web_apps.restart(choice['resourceGroup'], choice['name'])


def start_webapp(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Start a web app at random.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start start_webapp: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_webapp_at_random(filter, configuration, secrets)

    logger.debug("Starting web app: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.web_apps.start(choice['resourceGroup'], choice['name'])


def delete_webapp(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Delete a web app at random.

    ***Be aware**: Deleting a web app is an invasive action. You will not be
    able to recover the web app once you deleted it.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start delete_webapp: configuration='{}', filter='{}'".format(
            configuration, filter))

    choice = __fetch_webapp_at_random(filter, configuration, secrets)

    logger.debug("Deleting web app: {}".format(choice['name']))
    client = __init_client(secrets, configuration)
    client.web_apps.delete(choice['resourceGroup'], choice['name'])


def fetch_webapps(filter, configuration, secrets):
    webapps = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)
    if not webapps:
        logger.warning("No web apps found")
        raise FailedActivity("No web apps found")
    else:
        logger.debug(
            "Fetched web apps: {}".format(
                [x['name'] for x in webapps]))
    return webapps


###############################################################################
# Private helper functions
###############################################################################
def __fetch_webapp_at_random(filter, configuration, secrets):
    webapps = fetch_webapps(filter, configuration, secrets)
    choice = random.choice(webapps)
    return choice


def __init_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = WebSiteManagementClient(
            credentials=cred,
            subscription_id=subscription_id)

        return client
