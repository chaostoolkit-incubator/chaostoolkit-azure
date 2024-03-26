from unittest.mock import MagicMock, patch

import pytest
from chaoslib.exceptions import FailedActivity

import chaosazure
from chaosazure.machine.actions import (
    restart_machines,
    stop_machines,
    delete_machines,
    start_machines,
    stress_cpu,
    fill_disk,
    network_latency,
    burn_io,
)
from chaosazure.machine.constants import RES_TYPE_VM
from tests.data import machine_provider, config_provider, secrets_provider

CONFIG = {"azure": {"subscription_id": "***REMOVED***"}}

SECRETS = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
}

SECRETS_CHINA = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_CHINA_CLOUD",
}

MACHINE_ALPHA = {"name": "VirtualMachineAlpha", "resourceGroup": "group"}

MACHINE_BETA = {"name": "VirtualMachineBeta", "resourceGroup": "group"}


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_delete_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.begin_delete.call_count == 1


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_delete_one_machine_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_machines(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.virtual_machines.begin_delete.call_count == 1


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_delete_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA, MACHINE_BETA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.begin_delete.call_count == 2


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
def test_delete_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_machines(None, None, None)

    assert "No virtual machines found" in str(x.value)


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
def test_stop_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_machines(None, None, None)

    assert "No virtual machines found" in str(x.value)


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_stop_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.begin_power_off.call_count == 1


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_stop_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA, MACHINE_BETA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.begin_power_off.call_count == 2


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_restart_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    restart_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.begin_restart.call_count == 1


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_restart_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA, MACHINE_BETA]
    fetch.return_value = machines

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    restart_machines(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.virtual_machines.begin_restart.call_count == 2


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
def test_restart_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_machines(None, None, None)

    assert "No virtual machines found" in str(x.value)


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
def test_start_machine_with_no_machines(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_machines()

    assert "No virtual machines found" in str(x.value)


@patch("chaosazure.machine.actions.__fetch_machines", autospec=True)
@patch("chaosazure.machine.actions.__fetch_all_stopped_machines", autospec=True)
@patch("chaosazure.machine.actions.__compute_mgmt_client", autospec=True)
def test_start_machine(init, fetch_stopped, fetch_all):
    client = MagicMock()
    init.return_value = client


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
@patch.object(chaosazure.common.compute.command, "prepare", autospec=True)
@patch.object(chaosazure.common.compute.command, "run", autospec=True)
def test_stress_cpu(mocked_command_run, mocked_command_prepare, fetch):
    # arrange mocks
    mocked_command_prepare.return_value = "RunShellScript", "cpu_stress_test.sh"

    machine = machine_provider.provide_machine()
    machines = [machine]
    fetch.return_value = machines

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    stress_cpu(
        filter="where name=='some_linux_machine'",
        duration=60,
        timeout=60,
        configuration=config,
        secrets=secrets,
    )

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'", RES_TYPE_VM, secrets, config
    )
    mocked_command_prepare.assert_called_with(machine, "cpu_stress_test")
    mocked_command_run.assert_called_with(
        machine["resourceGroup"],
        machine,
        120,
        {
            "command_id": "RunShellScript",
            "script": ["cpu_stress_test.sh"],
            "parameters": [
                {"name": "duration", "value": 60},
            ],
        },
        secrets,
        config,
    )


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
@patch.object(chaosazure.common.compute.command, "prepare", autospec=True)
@patch.object(chaosazure.common.compute.command, "prepare_path", autospec=True)
@patch.object(chaosazure.common.compute.command, "run", autospec=True)
def test_fill_disk(
    mocked_command_run,
    mocked_command_prepare_path,
    mocked_command_prepare,
    fetch,
):
    # arrange mocks
    mocked_command_prepare.return_value = "RunShellScript", "fill_disk.sh"
    mocked_command_prepare_path.return_value = "/root/burn/hard"

    machine = machine_provider.provide_machine()
    machines = [machine]
    fetch.return_value = machines

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    fill_disk(
        filter="where name=='some_linux_machine'",
        duration=60,
        timeout=60,
        size=1000,
        path="/root/burn/hard",
        configuration=config,
        secrets=secrets,
    )

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'", RES_TYPE_VM, secrets, config
    )
    mocked_command_prepare.assert_called_with(machine, "fill_disk")
    mocked_command_run.assert_called_with(
        machine["resourceGroup"],
        machine,
        120,
        {
            "command_id": "RunShellScript",
            "script": ["fill_disk.sh"],
            "parameters": [
                {"name": "duration", "value": 60},
                {"name": "size", "value": 1000},
                {"name": "path", "value": "/root/burn/hard"},
            ],
        },
        secrets,
        config,
    )


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
@patch.object(chaosazure.common.compute.command, "prepare", autospec=True)
@patch.object(chaosazure.common.compute.command, "run", autospec=True)
def test_network_latency(mocked_command_run, mocked_command_prepare, fetch):
    # arrange mocks
    mocked_command_prepare.return_value = "RunShellScript", "network_latency.sh"

    machine = machine_provider.provide_machine()
    machines = [machine]
    fetch.return_value = machines

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    network_latency(
        filter="where name=='some_linux_machine'",
        duration=60,
        delay=200,
        jitter=50,
        timeout=60,
        configuration=config,
        secrets=secrets,
    )

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'", RES_TYPE_VM, secrets, config
    )
    mocked_command_prepare.assert_called_with(machine, "network_latency")
    mocked_command_run.assert_called_with(
        machine["resourceGroup"],
        machine,
        120,
        {
            "command_id": "RunShellScript",
            "script": ["network_latency.sh"],
            "parameters": [
                {"name": "duration", "value": 60},
                {"name": "delay", "value": 200},
                {"name": "jitter", "value": 50},
            ],
        },
        secrets,
        config,
    )


@patch("chaosazure.machine.actions.fetch_resources", autospec=True)
@patch.object(chaosazure.common.compute.command, "prepare", autospec=True)
@patch.object(chaosazure.common.compute.command, "run", autospec=True)
def test_burn_io(mocked_command_run, mocked_command_prepare, fetch):
    # arrange mocks
    mocked_command_prepare.return_value = "RunShellScript", "burn_io.sh"

    machine = machine_provider.provide_machine()
    machines = [machine]
    fetch.return_value = machines

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    burn_io(
        filter="where name=='some_linux_machine'",
        duration=60,
        configuration=config,
        secrets=secrets,
    )

    # assert
    fetch.assert_called_with(
        "where name=='some_linux_machine'", RES_TYPE_VM, secrets, config
    )
    mocked_command_prepare.assert_called_with(machine, "burn_io")
    mocked_command_run.assert_called_with(
        machine["resourceGroup"],
        machine,
        120,
        {
            "command_id": "RunShellScript",
            "script": ["burn_io.sh"],
            "parameters": [{"name": "duration", "value": 60}],
        },
        secrets,
        config,
    )
