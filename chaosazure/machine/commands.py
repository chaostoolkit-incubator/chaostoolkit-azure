def delete_machine_command(choice):
    command = ['vm', 'delete',
               '-g', choice['resourceGroup'],
               '-n', choice['name']]

    return command


def poweroff_machine_command(choice):
    command = ['vm', 'stop',
               '-g', choice['resourceGroup'],
               '-n', choice['name']]

    return command


def restart_machine_command(choice):
    command = ['vm', 'restart',
               '-g', choice['resourceGroup'],
               '-n', choice['name']]

    return command
