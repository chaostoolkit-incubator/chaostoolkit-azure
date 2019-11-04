from chaosazure import init_client


def fetch_vmss_instances(choice, configuration, secrets):
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
