from azure.mgmt.compute import ComputeManagementClient

from chaosazure import auth


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
            'instanceId': i.instance_id
        }
        results.append(m)
    return results


def init_client(secrets, configuration):
    with auth(secrets) as cred:
        subscription_id = configuration['azure']['subscription_id']
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id)

        return client
