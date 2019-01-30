from azure.mgmt.compute.v2018_10_01.models import VirtualMachineInstanceView, \
    InstanceViewStatus
from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.machine.actions import restart_machine, stop_machine, \
    delete_machine, start_machine

resource = {
    'name': 'chaos-machine',
    'resourceGroup': 'rg'}


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_delete_machine(init, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list
    m = MockComputeManagementClient()
    init.return_value = m

    delete_machine(None, None, None)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_delete_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_machine(None, None, None)

    assert "No virtual machines found" in str(x)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_stop_machine(init, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list
    m = MockComputeManagementClient()
    init.return_value = m

    stop_machine(None, None, None)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_stop_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_machine(None, None, None)

    assert "No virtual machines found" in str(x)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_restart_machine(init, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list
    m = MockComputeManagementClient()
    init.return_value = m

    restart_machine(None, None, None)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_restart_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_machine(None, None, None)

    assert "No virtual machines found" in str(x)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_start_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_machine()

    assert "No virtual machines found" in str(x)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_start_machine(init, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list
    m = MockComputeManagementClient()
    init.return_value = m

    start_machine(None, None, None)


class MockVirtualMachinesOperations(object):
    def power_off(self, resource_group, name):
        pass

    def delete(self, resource_group, name):
        pass

    def restart(self, resource_group, name):
        pass

    def start(self, resource_group, name):
        pass

    def instance_view(self, resource_group, name):
        statuses = []
        s = InstanceViewStatus(code='PowerState/Deallocated')
        statuses.append(s)
        return VirtualMachineInstanceView(statuses=statuses)


class MockComputeManagementClient(object):
    def __init__(self):
        self.operations = MockVirtualMachinesOperations()

    @property
    def virtual_machines(self):
        return self.operations
