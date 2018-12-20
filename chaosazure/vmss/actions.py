import random

from azure.mgmt.compute import ComputeManagementClient
from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import auth
from chaosazure.vmss.vmss_fetcher import fetch_vmss, fetch_vmss_instances

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

    vmss = fetch_vmss(filter, configuration, secrets)

    if not vmss:
        logger.warn("No virtual machine scale sets found")
        raise FailedActivity("No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = fetch_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        logger.warn("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    client = init_client(secrets, configuration)

    logger.debug(
        "Deleting instance: {}".format(choice_vmss_instance['name']))
    client.virtual_machine_scale_set_vms.delete(
        choice_vmss['resourceGroup'],
        choice_vmss['name'],
        choice_vmss_instance['instanceId'])


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
    vmss = fetch_vmss(filter, configuration, secrets)

    if not vmss:
        logger.warn("No virtual machine scale sets found")
        raise FailedActivity("No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = fetch_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        logger.warn("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    client = init_client(secrets, configuration)

    logger.debug(
        "Restarting instance: {}".format(choice_vmss_instance['name']))
    client.virtual_machine_scale_set_vms.restart(
        choice_vmss['resourceGroup'],
        choice_vmss['name'],
        choice_vmss_instance['instanceId'])


def stop_vmss(filter: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Power off a virtual machine scale set instance at random.
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
    vmss = fetch_vmss(filter, configuration, secrets)

    if not vmss:
        logger.warn("No virtual machine scale sets found")
        raise FailedActivity("No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = fetch_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        logger.warn("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    client = init_client(secrets, configuration)

    logger.debug(
        "Stopping instance: {}".format(choice_vmss_instance['name']))
    client.virtual_machine_scale_set_vms.power_off(
        choice_vmss['resourceGroup'],
        choice_vmss['name'],
        choice_vmss_instance['instanceId'])


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
    vmss = fetch_vmss(filter, configuration, secrets)

    if not vmss:
        logger.warn("No virtual machine scale sets found")
        raise FailedActivity("No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = fetch_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        logger.warn("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    client = init_client(secrets, configuration)

    logger.debug(
        "Deallocating instance: {}".format(choice_vmss_instance['name']))
    client.virtual_machine_scale_set_vms.deallocate(
        choice_vmss['resourceGroup'],
        choice_vmss['name'],
        choice_vmss_instance['instanceId'])


###############################################################################
# Private helper functions
###############################################################################
def init_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id)

        return client
