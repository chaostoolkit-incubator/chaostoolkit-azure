# -*- coding: utf-8 -*-
import random

from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosazure.cli.runner import execute
from chaosazure.machine.commands import restart_machine_command, \
    poweroff_machine_command, delete_machine_command
from chaosazure.machine.picker import pick_machines

__all__ = ["delete_machine", "poweroff_machine", "restart_machine"]


def delete_machine(configuration: Configuration = None,
                   secrets: Secrets = None, filter: str = None):
    """
    Delete a virtual machines at random.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start delete_machine: configuration='{}', filter='{}'"
                 .format(configuration, filter))

    machines = pick_machines(configuration, secrets, filter)
    choice = random.choice(machines)

    command = delete_machine_command(choice)
    execute(configuration, secrets, command)


def poweroff_machine(configuration: Configuration = None,
                     secrets: Secrets = None, filter: str = None):
    """
    Power off a virtual machines at random.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start poweroff_machine: configuration='{}', filter='{}'"
                 .format(configuration, filter))

    machines = pick_machines(configuration, secrets, filter)
    choice = random.choice(machines)

    command = poweroff_machine_command(choice)
    execute(configuration, secrets, command)


def restart_machine(configuration: Configuration = None,
                    secrets: Secrets = None, filter: str = None):
    """
    Restart a virtual machines at random.

    Parameters
    ----------
    filter : str
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start restart_machine: configuration='{}', filter='{}'"
                 .format(configuration, filter))

    machines = pick_machines(configuration, secrets, filter)
    choice = random.choice(machines)

    command = restart_machine_command(choice)
    execute(configuration, secrets, command)
