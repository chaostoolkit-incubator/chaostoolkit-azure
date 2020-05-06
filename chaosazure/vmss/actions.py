import os
from typing import Iterable, Mapping

from chaoslib import Configuration, Secrets
from logzero import logger

from chaosazure import init_client
from chaosazure.vmss import command
from chaosazure.vmss.vmss_fetcher import choose_vmss_at_random, \
    choose_vmss_instance_at_random, choose_vmss_instance

__all__ = [
    "delete_vmss", "restart_vmss", "stop_vmss", "deallocate_vmss",
    "burn_io", "fill_disk", "network_latency", "stress_vmss_instance_cpu"
]


def delete_vmss(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Delete a virtual machine scale set instance at random.

    **Be aware**: Deleting a VMSS instance is an invasive action. You will not
    be able to recover the VMSS instance once you deleted it.

     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start delete_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Deleting instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.delete(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def restart_vmss(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Restart a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start restart_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Restarting instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.restart(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def stop_vmss(filter: str = None,
              configuration: Configuration = None,
              instance_criteria: Iterable[Mapping[str, any]] = None,
              secrets: Secrets = None):
    """
    Stop a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    instance_criteria :  Iterable[Mapping[str, any]]
        Allows specification of criteria for selection of a given virtual
        machine scale set instance. If the instance_criteria is omitted,
        an instance will be chosen at random. All of the criteria within each
        item of the Iterable must match, i.e. AND logic is applied.
        The first item with all matching criterion will be used to select the
        instance.
        Criteria example:
        [
         {"name": "myVMSSInstance1"},
         {
          "name": "myVMSSInstance2",
          "instanceId": "2"
         }
         {"instanceId": "3"},
        ]
        If the instances include two items. One with name = myVMSSInstance4
        and instanceId = 2. The other with name = myVMSSInstance2 and
        instanceId = 3. The criteria {"instanceId": "3"} will be the first
        match since both the name and the instanceId did not match on the
        first criteria.
    """
    logger.debug(
        "Start stop_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = choose_vmss_at_random(filter, configuration, secrets)
    if not instance_criteria:
        vmss_instance = choose_vmss_instance_at_random(
            vmss, configuration, secrets)
    else:
        vmss_instance = choose_vmss_instance(
            vmss, configuration, instance_criteria, secrets)

    logger.debug(
        "Stopping instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.power_off(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def deallocate_vmss(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Deallocate a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Start deallocate_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    vmss_instance = choose_vmss_instance_at_random(
        vmss, configuration, secrets)

    logger.debug(
        "Deallocating instance: {}".format(vmss_instance['name']))
    client = init_client(secrets, configuration)
    client.virtual_machine_scale_set_vms.deallocate(
        vmss['resourceGroup'],
        vmss['name'],
        vmss_instance['instanceId'])


def stress_vmss_instance_cpu(filter: str = None,
                             duration: int = 120,
                             timeout: int = 60,
                             configuration: Configuration = None,
                             secrets: Secrets = None):
    """
    Stress CPU up to 100% at random machines.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage.
        Defaults to 120 seconds.
    timeout : int
        Additional wait time (in seconds) for stress operation to be completed.
        Getting and sending data from/to Azure may take some time so it's not
        recommended to set this value to less than 30s. Defaults to 60 seconds.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stress_vmss_instance_cpu("where resourceGroup=='rg'", configuration=c,
                    secrets=s)
    Stress all machines from the group 'rg'

    >>> stress_vmss_instance_cpu("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Stress the machine from the group 'rg' having the name 'name'

    >>> stress_vmss_instance_cpu("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Stress two machines at random from the group 'rg'
    """
    msg = "Starting stress_vmss_instance_cpu:" \
          " configuration='{}', filter='{}', duration='{}', timeout='{}'" \
        .format(configuration, filter, duration, timeout)
    logger.debug(msg)

    # TODO Place for improvement: Let the user decide what
    #  he wants to chaos engineer - not the function :)
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    machine = choose_vmss_instance_at_random(vmss, configuration, secrets)

    command_id, script_name = command.prepare(machine, 'cpu_stress_test')

    with open(os.path.join(os.path.dirname(__file__),
                           "../scripts", script_name)) as file:
        script_content = file.read()

    parameters = {
        'command_id': command_id,
        'script': [script_content],
        'parameters': [
            {'name': "duration", 'value': duration}
        ]
    }

    logger.debug("Stressing CPU of VMSS instance: '{}'"
                 .format(machine['name']))
    _timeout = duration + timeout
    _error_msg = "You may consider increasing timeout setting."
    command.run(
        vmss['resourceGroup'], vmss['name'], machine, _timeout, parameters,
        secrets, configuration, _error_msg)


def burn_io(filter: str = None,
            duration: int = 60,
            timeout: int = 60,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """
    Increases the Disk I/O operations per second of the VMSS machine.
    Similar to the burn_io action of the machine.actions module.
    """
    msg = "Starting burn_io: configuration='{}', filter='{}', duration='{}'," \
          " timeout='{}'".format(configuration, filter, duration, timeout)
    logger.debug(msg)

    # TODO Place for improvement: Let the user decide what
    #  he wants to chaos engineer - not the function :)
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    machine = choose_vmss_instance_at_random(vmss, configuration, secrets)

    command_id, script_name = command.prepare(machine, 'burn_io')

    with open(os.path.join(os.path.dirname(__file__),
                           "../scripts", script_name)) as file:
        script_content = file.read()

    parameters = {
        'command_id': command_id,
        'script': [script_content],
        'parameters': [
            {'name': "duration", 'value': duration}
        ]
    }

    logger.debug("Burning IO of VMSS instance: '{}'"
                 .format(machine['name']))
    _timeout = duration + timeout
    command.run(
        vmss['resourceGroup'], vmss['name'], machine, _timeout, parameters,
        secrets, configuration)


def fill_disk(filter: str = None,
              duration: int = 120,
              timeout: int = 60,
              size: int = 1000,
              path: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Fill the VMSS machine disk with random data. Similar to
    the fill_disk action of the machine.actions module.
    """
    msg = "Starting fill_disk: configuration='{}', filter='{}'," \
          " duration='{}', size='{}', path='{}', timeout='{}'" \
        .format(configuration, filter, duration, size, path, timeout)
    logger.debug(msg)

    # TODO Place for improvement: Let the user decide what
    #  he wants to chaos engineer - not the function :)
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    machine = choose_vmss_instance_at_random(vmss, configuration, secrets)

    command_id, script_name = command.prepare(machine, 'fill_disk')
    fill_path = command.prepare_path(machine, path)

    with open(os.path.join(os.path.dirname(__file__),
                           "../scripts", script_name)) as file:
        script_content = file.read()

    parameters = {
        'command_id': command_id,
        'script': [script_content],
        'parameters': [
            {'name': "duration", 'value': duration},
            {'name': "size", 'value': size},
            {'name': "path", 'value': fill_path}
        ]
    }

    logger.debug("Filling disk of VMSS instance: '{}'"
                 .format(machine['name']))
    _timeout = duration + timeout
    command.run(
        vmss['resourceGroup'], vmss['name'], machine, _timeout, parameters,
        secrets, configuration)


def network_latency(filter: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    timeout: int = 60,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Increases the response time of the virtual machine. Similar to
    the network_latency action of the machine.actions module.
    """
    msg = "Starting network_latency: configuration='{}', filter='{}'," \
          " duration='{}', delay='{}', jitter='{}', timeout='{}'"\
        .format(configuration, filter, duration, delay, jitter, timeout)
    logger.debug(msg)

    # TODO Place for improvement: Let the user decide what
    #  he wants to chaos engineer - not the function :)
    vmss = choose_vmss_at_random(filter, configuration, secrets)
    machine = choose_vmss_instance_at_random(vmss, configuration, secrets)

    command_id, script_name = command.prepare(machine, 'network_latency')

    with open(os.path.join(os.path.dirname(__file__),
                           "../scripts", script_name)) as file:
        script_content = file.read()

    parameters = {
        'command_id': command_id,
        'script': [script_content],
        'parameters': [
            {'name': "duration", 'value': duration},
            {'name': "delay", 'value': delay},
            {'name': "jitter", 'value': jitter}
        ]
    }

    logger.debug("Adding network latency of VMSS instance: '{}'"
                 .format(machine['name']))
    _timeout = duration + timeout
    command.run(
        vmss['resourceGroup'], vmss['name'], machine, _timeout, parameters,
        secrets, configuration)
