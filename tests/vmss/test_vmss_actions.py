from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.vmss.actions import delete_vmss, restart_vmss, stop_vmss, \
    deallocate_vmss

resource_vmss = {
    'name': 'chaos-vmss',
    'resourceGroup': 'rg'}

resource_vmss_instance = {
    'name': 'chaos-vmss-instance',
    'instanceId': '1'}


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_client', autospec=True)
def test_deallocate_vmss(client, fetch_instances, fetch_vmss):
    vmss_list = [resource_vmss]
    fetch_vmss.return_value = vmss_list

    instances_list = [resource_vmss_instance]
    fetch_instances.return_value = instances_list

    client.return_value = MockComputeManagementClient()

    deallocate_vmss(None, None, None)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
def test_deallocate_vmss_having_no_vmss_instances(fetch_instances, fetch_vmss):
    with pytest.raises(FailedActivity) as x:
        vmss_list = [resource_vmss]
        fetch_vmss.return_value = vmss_list

        instances_list = []
        fetch_instances.return_value = instances_list

        deallocate_vmss(None, None, None)

    assert "No virtual machine scale set instances found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
def test_deallocate_vmss_having_no_vmss(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        deallocate_vmss(None, None, None)

    assert "No virtual machine scale sets found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_client', autospec=True)
def test_stop_vmss(client, fetch_instances, fetch_vmss):
    vmss_list = [resource_vmss]
    fetch_vmss.return_value = vmss_list

    instances_list = [resource_vmss_instance]
    fetch_instances.return_value = instances_list

    client.return_value = MockComputeManagementClient()

    stop_vmss(None, None, None)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
def test_stop_vmss_having_no_vmss_instances(fetch_instances, fetch_vmss):
    with pytest.raises(FailedActivity) as x:
        vmss_list = [resource_vmss]
        fetch_vmss.return_value = vmss_list

        instances_list = []
        fetch_instances.return_value = instances_list

        stop_vmss(None, None, None)

    assert "No virtual machine scale set instances found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
def test_stop_vmss_having_no_vmss(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_vmss(None, None, None)

    assert "No virtual machine scale sets found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_client', autospec=True)
def test_restart_vmss(client, fetch_instances, fetch_vmss):
    vmss_list = [resource_vmss]
    fetch_vmss.return_value = vmss_list

    instances_list = [resource_vmss_instance]
    fetch_instances.return_value = instances_list

    client.return_value = MockComputeManagementClient()

    restart_vmss(None, None, None)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
def test_restart_vmss_having_no_vmss_instances(fetch_instances, fetch_vmss):
    with pytest.raises(FailedActivity) as x:
        vmss_list = [resource_vmss]
        fetch_vmss.return_value = vmss_list

        instances_list = []
        fetch_instances.return_value = instances_list

        restart_vmss(None, None, None)

    assert "No virtual machine scale set instances found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
def test_restart_vmss_having_no_vmss(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_vmss(None, None, None)

    assert "No virtual machine scale sets found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_client', autospec=True)
def test_delete_vmss(client, fetch_instances, fetch_vmss):
    vmss_list = [resource_vmss]
    fetch_vmss.return_value = vmss_list

    instances_list = [resource_vmss_instance]
    fetch_instances.return_value = instances_list

    client.return_value = MockComputeManagementClient()

    delete_vmss(None, None, None)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
@patch('chaosazure.vmss.actions.fetch_vmss_instances', autospec=True)
def test_delete_vmss_having_no_vmss_instances(fetch_instances, fetch_vmss):
    with pytest.raises(FailedActivity) as x:
        vmss_list = [resource_vmss]
        fetch_vmss.return_value = vmss_list

        instances_list = []
        fetch_instances.return_value = instances_list

        delete_vmss(None, None, None)

    assert "No virtual machine scale set instances found" in str(x)


@patch('chaosazure.vmss.actions.fetch_resources', autospec=True)
def test_delete_vmss_having_no_vmss(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_vmss(None, None, None)

    assert "No virtual machine scale sets found" in str(x)


class MockVirtualMachineScaleSetVMsOperations(object):
    def power_off(self, resource_group_name, scale_set_name, instance_id):
        pass

    def delete(self, resource_group_name, scale_set_name, instance_id):
        pass

    def restart(self, resource_group_name, scale_set_name, instance_id):
        pass

    def deallocate(self, resource_group_name, scale_set_name, instance_id):
        pass


class MockComputeManagementClient(object):
    def __init__(self):
        self.operations = MockVirtualMachineScaleSetVMsOperations()

    @property
    def virtual_machine_scale_set_vms(self):
        return self.operations
