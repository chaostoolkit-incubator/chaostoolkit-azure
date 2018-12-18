# -*- coding: utf-8 -*-
import random
import secrets
from typing import List, Any

from chaoslib import configuration
from chaoslib.types import Configuration, Secrets
from knack import config
from logzero import logger

from chaosazure.cli.runner import execute
from chaosazure.machine.commands import restart_machine_command, \
    poweroff_machine_command, delete_machine_command, start_machine_command
from chaosazure.machine.picker import pick_machines

__all__ = ["delete_machine", "poweroff_machine", "restart_machine",
           "start_machine"]

stopped_machines: List[Any] = []


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

    stopped_machines.append(choice)

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


def start_machine(configuration: Configuration = None,
                  secrets: Secrets = None):
    """
        Start all stopped virtual machines.
    """

    logger.debug("Start start_machine: configuration='{}'"
                 .format(configuration))
    logger.debug(
        "Found machines: {}".format([x['name'] for x in stopped_machines]))
    for machine in stopped_machines:
        command = start_machine_command(machine)
        execute(configuration, secrets, command)

    stopped_machines.clear()
