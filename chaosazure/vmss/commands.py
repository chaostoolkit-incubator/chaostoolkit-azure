def list_vmss_instances_command(choice):
    command = ['vmss', 'list-instances',
               '-g', choice['resourceGroup'],
               '-n', choice['name']]
    return command


def restart_vmss_instance_command(choice_vmss, choice_vmss_instance):
    command = ['vmss', 'restart',
               '-g', choice_vmss['resourceGroup'],
               '-n', choice_vmss['name'],
               '--instance-ids', choice_vmss_instance['instanceId']]
    return command


def poweroff_vmss_instance_command(choice_vmss, choice_vmss_instance):
    command = ['vmss', 'stop',
               '-g', choice_vmss['resourceGroup'],
               '-n', choice_vmss['name'],
               '--instance-ids', choice_vmss_instance['instanceId']]
    return command


def deallocate_vmss_instance_command(choice_vmss, choice_vmss_instance):
    command = ['vmss', 'deallocate',
               '-g', choice_vmss['resourceGroup'],
               '-n', choice_vmss['name'],
               '--instance-ids', choice_vmss_instance['instanceId']]
    return command
