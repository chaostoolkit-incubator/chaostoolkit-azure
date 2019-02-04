from azure.mgmt.compute.v2018_10_01.models import VirtualMachineInstanceView, \
    InstanceViewStatus, RunCommandResult
from unittest.mock import MagicMock, patch, mock_open

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.machine.actions import restart_machine, stop_machine, \
    delete_machine, start_machine, stress_cpu


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


def __get_resource(os_type='Windows'):
    return {
    'name': 'chaos-machine',
    'resourceGroup': 'rg',
    'properties': {
        'storageProfile': {
            'osDisk': {
                'osType': os_type
            }
        }}
    }


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_delete_machine(init, fetch):
    resource_list = [__get_resource()]
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
    resource_list = [__get_resource()]
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
    resource_list = [__get_resource()]
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
    resource_list = [__get_resource()]
    fetch.return_value = resource_list
    m = MockComputeManagementClient()
    init.return_value = m

    start_machine(None, None, None)


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_stress_cpu_on_lnx(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Linux')
    resource_list = [resource]
    fetch.return_value = resource_list
    # run command mocks
    poller = MagicMock()
    client.virtual_machines.run_command.return_value = poller
    result = MagicMock(spec=RunCommandResult)
    poller.result.return_value = result
    result.value = [InstanceViewStatus()]

    # act
    stress_cpu("where name=='some_linux_machine'", 60)

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'",
        "Microsoft.Compute/virtualMachines", None, None)
    open.assert_called_with(AnyStringWith("cpu_stress_test.sh"))
    client.virtual_machines.run_command.assert_called_with(
        resource['resourceGroup'],
        resource['name'],
        {
            'command_id': 'RunShellScript',
            'script': ['script'],
            'parameters': [{
                'name': 'duration',
                'value': 60
            }]
        })



@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_stress_cpu_on_win(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Windows')
    resource_list = [resource]
    fetch.return_value = resource_list
    # run command mocks
    poller = MagicMock()
    client.virtual_machines.run_command.return_value = poller
    result = MagicMock(spec=RunCommandResult)
    poller.result.return_value = result
    result.value = [InstanceViewStatus()]

    # act
    stress_cpu("where name=='some_windows_machine'", 60)

    # assert
    fetch.assert_called_with(
        "where name=='some_windows_machine'",
        "Microsoft.Compute/virtualMachines", None, None)
    open.assert_called_with(AnyStringWith("cpu_stress_test.ps1"))
    client.virtual_machines.run_command.assert_called_with(
        resource['resourceGroup'],
        resource['name'],
        {
            'command_id': 'RunPowerShellScript',
            'script': ['script'],
            'parameters': [{
                'name': 'duration',
                'value': 60
            }]
        })


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_stress_cpu_invalid_resource(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Invalid')
    resource_list = [resource]
    fetch.return_value = resource_list

    # act
    with pytest.raises(Exception) as ex:
        stress_cpu("where name=='some_machine'", 60)
    assert str(ex.value) == 'Unknown OS Type: invalid'


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__init_client', autospec=True)
def test_stress_cpu_timeout(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Windows')
    resource_list = [resource]
    fetch.return_value = resource_list
    # run command mocks
    poller = MagicMock()
    client.virtual_machines.run_command.return_value = poller
    poller.result.return_value = None

    # act & assert
    with pytest.raises(FailedActivity, match=r'stress_cpu operation did not '
                                             r'finish on time'):
        stress_cpu("where name=='some_windows_machine'", 60)


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
