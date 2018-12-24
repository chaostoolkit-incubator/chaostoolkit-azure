import random

from azure.mgmt.compute import ComputeManagementClient
from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import auth
from chaosazure.rgraph.resource_graph import fetch_resources
from chaosazure.vmss.constants import RES_TYPE_VMSS
from chaosazure.vmss.vmss_fetcher import fetch_vmss_instances

__all__ = ["delete_vmss", "restart_vmss", "stop_vmss", "deallocate_vmss"]


def delete_vmss(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Delete a virtual machine scale set instance at random.

    **Be aware**: Deleting a VMSS instance is an invasive action. You will not
    be able to recover the VMSS instance once you deleted it.

     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start delete_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Deleting instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.delete(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def restart_vmss(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Restart a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start restart_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Restarting instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.restart(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def stop_vmss(filter: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Stop a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start stop_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Stopping instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.power_off(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def deallocate_vmss(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Deallocate a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start deallocate_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Deallocating instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.deallocate(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


###############################################################################
# Private helper functions
###############################################################################
def choose_vmss_instance_at_random(vmss_choice, configuration, secrets):
    vmss_instances = fetch_vmss_instances(vmss_choice, configuration, secrets)
    if not vmss_instances:
        logger.warning("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")
    else:
        logger.debug(
            "Found virtual machine scale set instances: {}".format(
                [x['name'] for x in vmss_instances]))
    choice_vmss_instance = random.choice(vmss_instances)
    return choice_vmss_instance


def choose_vmss_at_random(filter, configuration, secrets):
    vmss = fetch_resources(filter, RES_TYPE_VMSS, secrets, configuration)
    if not vmss:
        logger.warning("No virtual machine scale sets found")
        raise FailedActivity("No virtual machine scale sets found")
    else:
        logger.debug(
            "Found virtual machine scale sets: {}".format(
                [x['name'] for x in vmss]))
    return random.choice(vmss)


def init_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id)

        return client
