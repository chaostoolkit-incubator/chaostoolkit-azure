import random

from logzero import logger


def pick_machine_randomly(subscribed_resource_groups, subscribed_instances,
                          configured_resource_groups=None):
    machines = pick_machines(subscribed_resource_groups, subscribed_instances,
                             configured_resource_groups)
    return random.choice(machines)


def pick_machines(subscribed_resource_groups, subscribed_machines,
                  configured_resource_groups=None):
    machines = []

    if not configured_resource_groups or configured_resource_groups is None:
        logger.info("Client will pick all subscribed machines")
        for machine in subscribed_machines:
            machines.append(machine)
    else:
        for resource_group in subscribed_resource_groups:
            if resource_group.name in configured_resource_groups:
                for machine in subscribed_machines:
                    machine_id_lower = machine.id.lower()
                    group_id_lower = resource_group.id.lower()
                    if machine_id_lower.startswith(group_id_lower):
                        machines.append(machine)

    return machines
