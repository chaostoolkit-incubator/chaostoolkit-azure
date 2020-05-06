from unittest.mock import MagicMock, patch, mock_open

import pytest
from azure.mgmt.compute.v2018_10_01.models import InstanceViewStatus, \
    RunCommandResult
from chaoslib.exceptions import FailedActivity

from chaosazure.machine.actions import restart_machines, stop_machines, \
    delete_machines, start_machines, stress_cpu, fill_disk, network_latency, \
    burn_io

CONFIG = {
    "azure": {
        "subscription_id": "***REMOVED***"
    }
}

SECRETS = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***"
}

SECRETS_CHINA = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_CHINA_CLOUD"
}

MACHINE_ALPHA = {
    'name': 'VirtualMachineAlpha',
    'resourceGroup': 'group'}

MACHINE_BETA = {
    'name': 'VirtualMachineBeta',
    'resourceGroup': 'group'}


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


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_delete_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.delete.call_count == 1


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_delete_one_machine_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_machines(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.virtual_machines.delete.call_count == 1


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_delete_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA, MACHINE_BETA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.delete.call_count == 2


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_delete_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_machines(None, None, None)

    assert "No virtual machines found" in str(x.value)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_stop_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_machines(None, None, None)

    assert "No virtual machines found" in str(x.value)


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_stop_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.power_off.call_count == 1


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_stop_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA, MACHINE_BETA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.power_off.call_count == 2


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_restart_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    restart_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.restart.call_count == 1


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_restart_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA, MACHINE_BETA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    restart_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.restart.call_count == 2


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_restart_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_machines(None, None, None)

    assert "No virtual machines found" in str(x.value)


@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
def test_start_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_machines()

    assert "No virtual machines found" in str(x.value)


@patch('chaosazure.machine.actions.__fetch_machines', autospec=True)
@patch('chaosazure.machine.actions.__fetch_all_stopped_machines',
       autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_start_machine(init, fetch_stopped, fetch_all):
    client = MagicMock()
    init.return_value = client


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
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
    stress_cpu(filter="where name=='some_linux_machine'", duration=60,
               configuration=CONFIG, secrets=SECRETS)

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'",
        "Microsoft.Compute/virtualMachines", SECRETS, CONFIG)
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
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
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
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
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
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
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


# def test_fill_disk(): fill_disk(filter="where resourceGroup=~'chaosworld'
# and name=='testWindows'",
# configuration=CONFIG, secrets=SECRETS)


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_fill_disk_on_lnx(init, fetch, open):
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
    fill_disk(filter="where name=='some_linux_machine'", duration=60, size=100,
              configuration=CONFIG, secrets=SECRETS)

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'",
        "Microsoft.Compute/virtualMachines", SECRETS, CONFIG)
    open.assert_called_with(AnyStringWith("fill_disk.sh"))
    client.virtual_machines.run_command.assert_called_with(
        resource['resourceGroup'],
        resource['name'],
        {
            'command_id': 'RunShellScript',
            'script': ['script'],
            'parameters': [
                {'name': 'duration', 'value': 60},
                {'name': 'size', 'value': 100},
                {'name': 'path', 'value': '/root/burn'}
            ]
        })


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_fill_disk_on_win(init, fetch, open):
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
    fill_disk("where name=='some_windows_machine'", 60, size=100)

    # assert
    fetch.assert_called_with(
        "where name=='some_windows_machine'",
        "Microsoft.Compute/virtualMachines", None, None)
    open.assert_called_with(AnyStringWith("fill_disk.ps1"))
    client.virtual_machines.run_command.assert_called_with(
        resource['resourceGroup'],
        resource['name'],
        {
            'command_id': 'RunPowerShellScript',
            'script': ['script'],
            'parameters': [
                {'name': 'duration', 'value': 60},
                {'name': 'size', 'value': 100},
                {'name': 'path', 'value': 'C:/burn'}
            ]
        })


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_fill_disk_invalid_resource(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Invalid')
    resource_list = [resource]
    fetch.return_value = resource_list

    # act
    with pytest.raises(Exception) as ex:
        fill_disk("where name=='some_machine'", 60, 100)
    assert str(ex.value) == 'Unknown OS Type: invalid'


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_fill_disk_timeout(init, fetch, open):
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
    with pytest.raises(FailedActivity, match=r'fill_disk operation did not '
                                             r'finish on time'):
        fill_disk("where name=='some_windows_machine'", 60, 100)


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_network_latency_on_lnx(init, fetch, open):
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
    network_latency(filter="where name=='some_linux_machine'", duration=60,
                    delay=200, jitter=50, configuration=CONFIG,
                    secrets=SECRETS)

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'",
        "Microsoft.Compute/virtualMachines", SECRETS, CONFIG)
    open.assert_called_with(AnyStringWith("network_latency.sh"))
    client.virtual_machines.run_command.assert_called_with(
        resource['resourceGroup'],
        resource['name'],
        {
            'command_id': 'RunShellScript',
            'script': ['script'],
            'parameters': [
                {'name': 'duration', 'value': 60},
                {'name': 'delay', 'value': 200},
                {'name': 'jitter', 'value': 50}
            ]
        })


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_network_latency_invalid_resource(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Invalid')
    resource_list = [resource]
    fetch.return_value = resource_list

    # act
    with pytest.raises(Exception) as ex:
        fill_disk("where name=='some_machine'", 60, 200, 50)
    assert str(ex.value) == 'Unknown OS Type: invalid'


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_network_latency_timeout(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Linux')
    resource_list = [resource]
    fetch.return_value = resource_list
    # run command mocks
    poller = MagicMock()
    client.virtual_machines.run_command.return_value = poller
    poller.result.return_value = None

    # act & assert
    with pytest.raises(FailedActivity, match=r'network_latency operation '
                                             r'did not finish on time'):
        network_latency("where name=='some_linux_machine'", 60, 200, 50)


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_burn_io_on_lnx(init, fetch, open):
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
    burn_io(filter="where name=='some_linux_machine'", duration=60,
            configuration=CONFIG, secrets=SECRETS)

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'",
        "Microsoft.Compute/virtualMachines", SECRETS, CONFIG)
    open.assert_called_with(AnyStringWith("burn_io.sh"))
    client.virtual_machines.run_command.assert_called_with(
        resource['resourceGroup'],
        resource['name'],
        {
            'command_id': 'RunShellScript',
            'script': ['script'],
            'parameters': [
                {'name': 'duration', 'value': 60}
            ]
        })


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_burn_io_invalid_resource(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Invalid')
    resource_list = [resource]
    fetch.return_value = resource_list

    # act
    with pytest.raises(Exception) as ex:
        burn_io("where name=='some_machine'", 60)
    assert str(ex.value) == 'Unknown OS Type: invalid'


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaosazure.machine.actions.fetch_resources', autospec=True)
@patch('chaosazure.machine.actions.__compute_mgmt_client', autospec=True)
def test_burn_io_timeout(init, fetch, open):
    # arrange mocks
    client = MagicMock()
    init.return_value = client
    resource = __get_resource(os_type='Linux')
    resource_list = [resource]
    fetch.return_value = resource_list
    # run command mocks
    poller = MagicMock()
    client.virtual_machines.run_command.return_value = poller
    poller.result.return_value = None

    # act & assert
    with pytest.raises(FailedActivity, match=r'burn_io operation did not '
                                             r'finish on time'):
        burn_io("where name=='some_linux_machine'", 60)
