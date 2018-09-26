import random

from logzero import logger


def pick_machine_randomly(subscribed_resource_groups, subscribed_instances, configuration):
    all_instances = pick_machines(subscribed_resource_groups, subscribed_instances, configuration)
    return random.choice(all_instances)


def pick_machines(subscribed_resource_groups, subscribed_instances, configuration=None):
    picked_instances = []

    if not configuration['resource_groups'] or configuration is None:
        logger.info("Client will pick all subscribed machines")
        for instance in subscribed_instances:
            picked_instances.append(instance)
    else:
        configured_resource_groups = configuration['resource_groups'].split(',')
        for resource_group in subscribed_resource_groups:
            if resource_group.name in configured_resource_groups:
                for instance in subscribed_instances:
                    if instance.id.lower().startswith(resource_group.id.lower()):
                        picked_instances.append(instance)

    return picked_instances
