from unittest.mock import patch

import chaosazure
from chaosazure.vmss.actions import delete_vmss, restart_vmss, stop_vmss, \
    deallocate_vmss, stress_vmss_instance_cpu, network_latency, burn_io, fill_disk
from tests.data import config_provider, secrets_provider, vmss_provider


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_compute_management_client', autospec=True)
def test_deallocate_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    fetch_vmss.return_value = scale_sets

    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    deallocate_vmss(None, None, None)


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_compute_management_client', autospec=True)
def test_stop_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    stop_vmss(None, None, None, None)


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_compute_management_client', autospec=True)
def test_restart_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    restart_vmss(None, None, None)


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('chaosazure.vmss.actions.init_compute_management_client', autospec=True)
def test_delete_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    delete_vmss(None, None, None)


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


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch.object(chaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(chaosazure.common.compute.command, 'run', autospec=True)
def test_stress_cpu(mocked_command_run, mocked_command_prepare, fetch_instance, fetch_vmss):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'cpu_stress_test.sh'

    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instance.return_value = instances

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    stress_vmss_instance_cpu(
        filter="where name=='some_random_instance'",
        duration=60, timeout=60, configuration=config, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", config, secrets)
    fetch_instance.assert_called_with(scale_set, None, config, secrets)
    mocked_command_prepare.assert_called_with(instance, 'cpu_stress_test')
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, 120,
        {
            'command_id': 'RunShellScript',
            'script': ['cpu_stress_test.sh'],
            'parameters': [
                {'name': "duration", 'value': 60},
            ]
        },
        secrets, config
    )


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch.object(chaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(chaosazure.common.compute.command, 'run', autospec=True)
def test_network_latency(mocked_command_run, mocked_command_prepare, fetch_instances, fetch_vmss):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'network_latency.sh'

    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    network_latency(
        filter="where name=='some_random_instance'",
        duration=60, timeout=60, delay=200, jitter=50,
        configuration=config, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", config, secrets)
    fetch_instances.assert_called_with(scale_set, None, config, secrets)
    mocked_command_prepare.assert_called_with(instance, 'network_latency')
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, 120,
        {
            'command_id': 'RunShellScript',
            'script': ['network_latency.sh'],
            'parameters': [
                {'name': "duration", 'value': 60},
                {'name': "delay", 'value': 200},
                {'name': "jitter", 'value': 50}
            ]
        },
        secrets, config
    )


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch.object(chaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(chaosazure.common.compute.command, 'run', autospec=True)
def test_burn_io(mocked_command_run, mocked_command_prepare, fetch_instances, fetch_vmss):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'burn_io.sh'

    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    burn_io(filter="where name=='some_random_instance'",
            duration=60, configuration=config, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", config, secrets)
    fetch_instances.assert_called_with(scale_set, None, config, secrets)
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, 120,
        {
            'command_id': 'RunShellScript',
            'script': ['burn_io.sh'],
            'parameters': [
                {'name': 'duration', 'value': 60}
            ]
        },
        secrets, config
    )


@patch('chaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('chaosazure.vmss.actions.fetch_instances', autospec=True)
@patch.object(chaosazure.common.compute.command, 'prepare_path', autospec=True)
@patch.object(chaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(chaosazure.common.compute.command, 'run', autospec=True)
def test_fill_disk(mocked_command_run, mocked_command_prepare,
                   mocked_command_prepare_path, fetch_instances, fetch_vmss):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'fill_disk.sh'
    mocked_command_prepare_path.return_value = '/root/burn/hard'

    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    # act
    fill_disk(filter="where name=='some_random_instance'",
              duration=60, timeout=60, size=1000,
              path='/root/burn/hard', configuration=config, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", config, secrets)
    fetch_instances.assert_called_with(scale_set, None, config, secrets)
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, 120,
        {
            'command_id': 'RunShellScript',
            'script': ['fill_disk.sh'],
            'parameters': [
                {'name': "duration", 'value': 60},
                {'name': "size", 'value': 1000},
                {'name': "path", 'value': '/root/burn/hard'}
            ]
        },
        secrets, config
    )
