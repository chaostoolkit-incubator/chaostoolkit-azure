from chaosazure.machine.commands import delete_machine_command, \
    poweroff_machine_command, restart_machine_command, start_machine_command

TESTED_RESOURCE = "Microsoft.ContainerService/managedClusters"


def test_delete_machine_command():
    machine = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    command = delete_machine_command(machine)

    assert len(command) == 7
    assert command[1] == 'delete'
    assert command[3] == machine['resourceGroup']
    assert command[5] == machine['name']


def test_poweroff_machine_command():
    machine = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    command = poweroff_machine_command(machine)

    assert len(command) == 6
    assert command[1] == 'stop'
    assert command[3] == machine['resourceGroup']
    assert command[5] == machine['name']


def test_restart_machine_command():
    machine = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    command = restart_machine_command(machine)

    assert len(command) == 6
    assert command[1] == 'restart'
    assert command[3] == machine['resourceGroup']
    assert command[5] == machine['name']


def test_start_machine_command():
    machine = {
        'name': 'myname',
        'resourceGroup': 'myresourcegroup'
    }
    command = start_machine_command(machine)
    assert len(command) == 6
    assert command[1] == 'start'
    assert command[3] == machine['resourceGroup']
    assert command[5] == machine['name']
