from typing import Iterable, Mapping

from chaoslib import Configuration, Secrets
from logzero import logger

from chaosazure import init_compute_management_client
from chaosazure.common import cleanse
from chaosazure.common.compute import command
from chaosazure.vmss.fetcher import fetch_vmss, fetch_instances
from chaosazure.vmss.records import Records

__all__ = [
    "delete_vmss", "restart_vmss", "stop_vmss", "deallocate_vmss",
    "burn_io", "fill_disk", "network_latency", "stress_vmss_instance_cpu"
]


def delete_vmss(filter: str = None,
                instance_criteria: Iterable[Mapping[str, any]] = None,
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
        "Starting delete_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            logger.debug(
                "Deleting instance: {}".format(instance['name']))
            client = init_compute_management_client(secrets, configuration)
            client.virtual_machine_scale_set_vms.delete(
                scale_set['resourceGroup'],
                scale_set['name'],
                instance['instance_id'])
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def restart_vmss(filter: str = None,
                 instance_criteria: Iterable[Mapping[str, any]] = None,
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
        "Starting restart_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            logger.debug(
                "Restarting instance: {}".format(instance['name']))
            client = init_compute_management_client(secrets, configuration)
            client.virtual_machine_scale_set_vms.restart(
                scale_set['resourceGroup'],
                scale_set['name'],
                instance['instance_id'])
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def stop_vmss(filter: str = None,
              instance_criteria: Iterable[Mapping[str, any]] = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Stops instances from the filtered scale set either at random or by
     a defined instance criteria.
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
        "Starting stop_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            logger.debug(
                "Stopping instance: {}".format(instance['name']))
            client = init_compute_management_client(secrets, configuration)
            client.virtual_machine_scale_set_vms.power_off(
                scale_set['resourceGroup'],
                scale_set['name'],
                instance['instance_id'])
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def deallocate_vmss(filter: str = None,
                    instance_criteria: Iterable[Mapping[str, any]] = None,
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
        "Starting deallocate_vmss: configuration='{}', filter='{}'".format(
            configuration, filter))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            logger.debug(
                "Deallocating instance: {}".format(instance['name']))
            client = init_compute_management_client(secrets, configuration)
            client.virtual_machine_scale_set_vms.deallocate(
                scale_set['resourceGroup'],
                scale_set['name'],
                instance['instance_id'])
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def stress_vmss_instance_cpu(
        filter: str = None,
        duration: int = 120,
        timeout: int = 60,
        instance_criteria: Iterable[Mapping[str, any]] = None,
        configuration: Configuration = None,
        secrets: Secrets = None):
    logger.warn(
        "Deprecated usage of activity 'stress_vmss_instance_cpu'."
        " Please use activity 'stress_cpu' in favor since this"
        " activity will be removed in a future release.")
    return stress_cpu(
        filter, duration, timeout, instance_criteria, configuration, secrets)


def stress_cpu(filter: str = None,
               duration: int = 120,
               timeout: int = 60,
               instance_criteria: Iterable[Mapping[str, any]] = None,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """
    Stresses the CPU of a random VMSS instances in your selected VMSS.
    Similar to the stress_cpu action of the machine.actions module.

    Parameters
    ----------
    filter : str, optional
        Filter the VMSS. If the filter is omitted all VMSS in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage.
        Defaults to 120 seconds.
    timeout : int
        Additional wait time (in seconds) for stress operation to be completed.
        Getting and sending data from/to Azure may take some time so it's not
        recommended to set this value to less than 30s. Defaults to 60 seconds.
    """
    logger.debug(
        "Starting stress_vmss_instance_cpu:"
        " configuration='{}', filter='{}',"
        " duration='{}', timeout='{}'".format(
            configuration, filter, duration, timeout))

    vmss_records = Records()
    vmss = fetch_vmss(filter, configuration, secrets)
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            command_id, script_content = command.prepare(instance,
                                                         'cpu_stress_test')
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration}
                ]
            }

            logger.debug(
                "Stressing CPU of VMSS instance: '{}'".format(
                    instance['instance_id']))
            _timeout = duration + timeout
            command.run(
                scale_set['resourceGroup'], instance, _timeout, parameters,
                secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def burn_io(filter: str = None,
            duration: int = 60,
            timeout: int = 60,
            instance_criteria: Iterable[Mapping[str, any]] = None,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """
    Increases the Disk I/O operations per second of the VMSS machine.
    Similar to the burn_io action of the machine.actions module.
    """
    logger.debug(
        "Starting burn_io: configuration='{}', filter='{}', duration='{}',"
        " timeout='{}'".format(configuration, filter, duration, timeout))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            command_id, script_content = command.prepare(instance, 'burn_io')
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration}
                ]
            }

            logger.debug(
                "Burning IO of VMSS instance: '{}'".format(instance['name']))
            _timeout = duration + timeout
            command.run(
                scale_set['resourceGroup'], instance, _timeout, parameters,
                secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def fill_disk(filter: str = None,
              duration: int = 120,
              timeout: int = 60,
              size: int = 1000,
              path: str = None,
              instance_criteria: Iterable[Mapping[str, any]] = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Fill the VMSS machine disk with random data. Similar to
    the fill_disk action of the machine.actions module.
    """
    logger.debug(
        "Starting fill_disk: configuration='{}', filter='{}',"
        " duration='{}', size='{}', path='{}', timeout='{}'".format(
            configuration, filter, duration, size, path, timeout))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            command_id, script_content = command.prepare(instance,
                                                         'fill_disk')
            fill_path = command.prepare_path(instance, path)

            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration},
                    {'name': "size", 'value': size},
                    {'name': "path", 'value': fill_path}
                ]
            }

            logger.debug(
                "Filling disk of VMSS instance: '{}'".format(
                    instance['name']))
            _timeout = duration + timeout
            command.run(
                scale_set['resourceGroup'], instance, _timeout, parameters,
                secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')


def network_latency(filter: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    timeout: int = 60,
                    instance_criteria: Iterable[Mapping[str, any]] = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Increases the response time of the virtual machine. Similar to
    the network_latency action of the machine.actions module.
    """
    logger.debug(
        "Starting network_latency: configuration='{}', filter='{}',"
        " duration='{}', delay='{}', jitter='{}', timeout='{}'".format(
            configuration, filter, duration, delay, jitter, timeout))

    vmss = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()
    for scale_set in vmss:
        instances_records = Records()
        instances = fetch_instances(scale_set, instance_criteria,
                                    configuration, secrets)

        for instance in instances:
            command_id, script_content = command.prepare(
                instance, 'network_latency')
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration},
                    {'name': "delay", 'value': delay},
                    {'name': "jitter", 'value': jitter}
                ]
            }

            logger.debug(
                "Increasing the latency of VMSS instance: '{}'".format(
                    instance['name']))
            _timeout = duration + timeout
            command.run(
                scale_set['resourceGroup'], instance, _timeout, parameters,
                secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        scale_set['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(scale_set))

    return vmss_records.output_as_dict('resources')
