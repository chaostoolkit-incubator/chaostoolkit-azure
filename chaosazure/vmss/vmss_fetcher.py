import random
from typing import Any, Dict, Iterable, Mapping, List

from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import init_client
from chaosazure.rgraph.resource_graph import fetch_resources
from chaosazure.vmss.constants import RES_TYPE_VMSS


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


def choose_vmss_instance(vmss_choice: dict,
                         configuration: Configuration = None,
                         instance_criteria: Iterable[Mapping[str, any]] = None,
                         secrets: Secrets = None) -> Dict[str, Any]:
    vmss_instances = fetch_vmss_instances(vmss_choice, configuration, secrets)
    if not vmss_instances:
        logger.debug("No virtual machine scale set instances found")
        raise FailedActivity("No virtual machine scale set instances found")
    else:
        logger.debug(
            "Found virtual machine scale set instances: {}".format(
                [x['name'] for x in vmss_instances]))

    choice_vmss_instance = None
    for vmss in vmss_instances:
        if vmss_matches_criteria(vmss, instance_criteria):
            choice_vmss_instance = vmss
            break

    if not choice_vmss_instance:
        logger.debug("No virtual machine scale set instance found for "
                     "virtual machine scale set %s and criteria %s"
                     % (vmss, instance_criteria))
        raise FailedActivity("No virtual machine scale set instances found for"
                             " criteria")

    logger.warning("Attempting to stop instance with name %s"
                   % choice_vmss_instance['name'])

    return choice_vmss_instance


def vmss_matches_criteria(vmss: dict,
                          instance_criteria:
                          Iterable[Mapping[str, any]] = None):
    for criteria in instance_criteria:
        logger.debug("Checking criteria %s" % criteria)
        found_mismatch = False
        for key, value in criteria.items():
            if vmss[key] != value:
                found_mismatch = True
                break
        if not found_mismatch:
            logger.debug("Matching criteria %s" % criteria)
            return True

    return False


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


def fetch_vmss_instances(choice, configuration, secrets) -> List[Dict]:
    vmss_instances = []
    client = init_client(secrets, configuration)
    pages = client.virtual_machine_scale_set_vms.list(
        choice['resourceGroup'], choice['name'])
    first_page = pages.advance_page()
    vmss_instances.extend(list(first_page))

    while True:
        try:
            page = pages.advance_page()
            vmss_instances.extend(list(page))
        except StopIteration:
            break

    results = __parse_vmss_instances_result(vmss_instances)
    return results


###############################################################################
# Private helper functions
###############################################################################
def __parse_vmss_instances_result(instances):
    results = []
    for i in instances:
        m = {
            'name': i.name,
            'instanceId': i.instance_id,
            'osType': i.storage_profile.os_disk.os_type.lower()
        }
        results.append(m)
    return results
