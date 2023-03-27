# -*- coding: utf-8 -*-
import re

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure import init_netapp_management_client
from chaosazure.common import cleanse
from chaosazure.netapp.constants import RES_TYPE_SRV_NV
from chaosazure.common.resources.graph import fetch_resources

__all__ = ["delete_netapp_volumes"]

from chaosazure.vmss.records import Records


def delete_netapp_volumes(filter: str = None,
                          configuration: Configuration = None,
                          secrets: Secrets = None):
    """
    Delete netapp volumes at random.

    **Be aware**: Deleting a netapp volume is a invasive action. You will not be
    able to recover the netapp volume once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the netapp volumes. If the filter is omitted all netapp volumes in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_netapp_volumes("where resourceGroup=='rg'", c, s)
    Delete all netapp volumes from the group 'rg'

    >>> delete_netapp_volumes("where resourceGroup=='rg' and name='name'", c, s)
    Delete the netapp volumes from the group 'rg' having the name 'name'

    >>> delete_netapp_volumes("where resourceGroup=='rg' | sample 2", c, s)
    Delete two netapp volumes at random from the group 'rg'
    """
    logger.debug(
        "Start delete_netapp_volumes: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    netapp_volumes = __fetch_netapp_volumes(filter, configuration, secrets)
    client = __netapp_mgmt_client(secrets, configuration)
    netapp_volumes_records = Records()

    for nv in netapp_volumes:
        group = nv['resourceGroup']
        full_name = nv['name']
        account_name = re.search(r"^([^\/]*)\/", full_name).group(1)
        pool_name = re.search(r"\/([^\/]*)\/", full_name).group(1)
        volume_name = re.search(r"\/([^\/]*)$", full_name).group(1)
        client.volumes.begin_delete(group, account_name, pool_name, volume_name)
        netapp_volumes_records.add(cleanse.netapp_volume(nv))

    return netapp_volumes_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################


def __fetch_netapp_volumes(filter, configuration, secrets) -> []:
    netapp_volumes = fetch_resources(filter, RES_TYPE_SRV_NV, secrets, configuration)
    if not netapp_volumes:
        logger.warning("No Netapp volumes found")
        raise FailedActivity("No Netapp volumes found")
    else:
        logger.debug(
            "Fetched netapp volumes: {}".format(
                [n['name'] for n in netapp_volumes]))
    return netapp_volumes


def __netapp_mgmt_client(secrets, configuration):
    return init_netapp_management_client(secrets, configuration)
