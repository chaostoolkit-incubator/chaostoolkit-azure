import random
from typing import Any, Dict, Iterable, Mapping, List

from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import init_compute_management_client
from chaosazure.common.resources.graph import fetch_resources
from chaosazure.vmss.constants import RES_TYPE_VMSS


def fetch_instances(scale_set, instance_criteria,
                    configuration, secrets) -> List[Dict[str, Any]]:
    if not instance_criteria:
        instance = __random_instance_from(
            scale_set, configuration, secrets)
        result = [instance]

    else:
        result = instances_by_criteria(
            scale_set, configuration, instance_criteria, secrets)

    return result


def instances_by_criteria(
        vmss_choice: dict,
        configuration: Configuration = None,
        instance_criteria: Iterable[Mapping[str, any]] = None,
        secrets: Secrets = None) -> List[Dict[str, Any]]:
    result = []
    instances = __fetch_vmss_instances(vmss_choice, configuration, secrets)

    for instance in instances:
        if __is_criteria_matched(instance, instance_criteria):
            result.append(instance)

    if len(result) == 0:
        raise FailedActivity(
            "No VMSS instance found for criteria '{}'".format(
                instance_criteria))

    return result


def fetch_vmss(filter, configuration, secrets) -> List[dict]:
    vmss = fetch_resources(filter, RES_TYPE_VMSS, secrets, configuration)

    if not vmss:
        raise FailedActivity("No VMSS found")

    else:
        logger.debug(
            "Fetched VMSS: {}".format([set['name'] for set in vmss]))

    return vmss


#############################################################################
# Private helper functions
#############################################################################
def __fetch_vmss_instances(choice, configuration, secrets) -> List[Dict]:
    vmss_instances = []
    client = init_compute_management_client(secrets, configuration)
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

    results = __parse_vmss_instances_result(vmss_instances, choice)
    return results


def __random_instance_from(
        scale_set,
        configuration,
        secrets) -> Dict[str, Any]:
    instances = __fetch_vmss_instances(
        scale_set, configuration, secrets)
    if not instances:
        raise FailedActivity("No VMSS instances found")
    else:
        logger.debug(
            "Found VMSS instances: {}".format(
                [x['name'] for x in instances]))

    return random.choice(instances)


def __is_criteria_matched(instance: dict,
                          criteria: Iterable[Mapping[str, any]] = None):
    for criterion in criteria:
        mismatch = False

        for key, value in criterion.items():
            if instance[key] != value:
                mismatch = True
                break

        if not mismatch:
            return True

    return False


def __parse_vmss_instances_result(instances, vmss: dict) -> List[Dict]:
    results = []
    for instance in instances:
        instance_as_dict = instance.as_dict()
        instance_as_dict['scale_set'] = vmss['name']
        results.append(instance_as_dict)
    return results
