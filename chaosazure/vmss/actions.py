import random
from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger
from chaosazure.cli.runner import execute
from chaosazure.vmss.commands import restart_vmss_instance_command, \
    poweroff_vmss_instance_command, deallocate_vmss_instance_command, \
    delete_vmss_instance_command
from chaosazure.vmss.picker import pick_vmss, pick_vmss_instances

__all__ = ["delete_vmss", "restart_vmss", "poweroff_vmss", "deallocate_vmss"]


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
    vmss = pick_vmss(filter, configuration, secrets)

    if not vmss:
        raise FailedActivity(
            "No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = pick_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        raise FailedActivity(
            "No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    command = delete_vmss_instance_command(choice_vmss, choice_vmss_instance)
    execute(configuration, secrets, command)


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
    vmss = pick_vmss(filter, configuration, secrets)

    if not vmss:
        raise FailedActivity(
            "No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = pick_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        raise FailedActivity(
            "No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    command = restart_vmss_instance_command(choice_vmss, choice_vmss_instance)
    execute(configuration, secrets, command)


def poweroff_vmss(filter: str = None,
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
        "Start poweroff_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = pick_vmss(filter, configuration, secrets)

    if not vmss:
        raise FailedActivity(
            "No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = pick_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        raise FailedActivity(
            "No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    command = poweroff_vmss_instance_command(choice_vmss, choice_vmss_instance)
    execute(configuration, secrets, command)


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
    vmss = pick_vmss(filter, configuration, secrets)

    if not vmss:
        raise FailedActivity(
            "No virtual machine scale sets found")

    choice_vmss = random.choice(vmss)
    vmss_instances = pick_vmss_instances(choice_vmss, configuration, secrets)

    if not vmss_instances:
        raise FailedActivity(
            "No virtual machine scale set instances found")

    choice_vmss_instance = random.choice(vmss_instances)
    command = deallocate_vmss_instance_command(
        choice_vmss, choice_vmss_instance)
    execute(configuration, secrets, command)
