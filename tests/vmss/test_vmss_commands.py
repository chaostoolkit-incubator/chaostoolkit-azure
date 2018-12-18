from chaosazure.vmss.commands import list_vmss_instances_command, \
    restart_vmss_instance_command, poweroff_vmss_instance_command, \
    deallocate_vmss_instance_command, delete_vmss_instance_command


def test_list_vmss_instances_command():
    vmss_instance = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    command = list_vmss_instances_command(vmss_instance)

    assert len(command) == 6
    assert command[1] == 'list-instances'
    assert command[3] == vmss_instance['resourceGroup']
    assert command[5] == vmss_instance['name']


def test_delete_vmss_instance_command():
    vmss = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    vmss_instance = {
        'instanceId': 1,
    }
    command = delete_vmss_instance_command(vmss, vmss_instance)

    assert len(command) == 8
    assert command[1] == 'delete-instances'
    assert command[3] == vmss['resourceGroup']
    assert command[5] == vmss['name']
    assert command[7] == vmss_instance['instanceId']


def test_restart_vmss_instance_command():
    vmss = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    vmss_instance = {
        'instanceId': 1,
    }
    command = restart_vmss_instance_command(vmss, vmss_instance)

    assert len(command) == 8
    assert command[1] == 'restart'
    assert command[3] == vmss['resourceGroup']
    assert command[5] == vmss['name']
    assert command[7] == vmss_instance['instanceId']


def test_poweroff_vmss_instance_command():
    vmss = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    vmss_instance = {
        'instanceId': 1,
    }
    command = poweroff_vmss_instance_command(vmss, vmss_instance)

    assert len(command) == 8
    assert command[1] == 'stop'
    assert command[3] == vmss['resourceGroup']
    assert command[5] == vmss['name']
    assert command[7] == vmss_instance['instanceId']


def test_deallocate_vmss_instance_command():
    vmss = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    vmss_instance = {
        'instanceId': 1,
    }
    command = deallocate_vmss_instance_command(vmss, vmss_instance)

    assert len(command) == 8
    assert command[1] == 'deallocate'
    assert command[3] == vmss['resourceGroup']
    assert command[5] == vmss['name']
    assert command[7] == vmss_instance['instanceId']
