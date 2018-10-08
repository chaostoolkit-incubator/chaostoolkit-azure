from chaosazure.machine.picker import pick_machines


def test_pick_machines_with_empty_arguments():
    subscribed_resource_groups = []
    subscribed_machines = []
    machines = pick_machines(subscribed_resource_groups, subscribed_machines)

    assert len(machines) == 0


def test_pick_machines_with_no_subscribed_machines():
    subscribed_resource_groups = [MyResourceGroup(name='res_group_one', location='centralus'),
                                  MyResourceGroup(name='res_group_two', location='centralus')]
    subscribed_machines = []
    configured_resource_groups = 'res_group_one,res_group_two'.split(',')
    machines = pick_machines(subscribed_resource_groups, subscribed_machines, configured_resource_groups)

    assert len(machines) == 0


def test_pick_machines_with_one_fitting_vm():
    subscribed_resource_groups = [MyResourceGroup(id='1234/res_group_one', name='res_group_one'),
                                  MyResourceGroup(id='9876/res_group_two', name='res_group_two')]
    subscribed_machines = [MyVirtualMachine(id='1234/res_group_one/myvmname')]
    configured_resource_groups = 'res_group_one,res_group_two'.split(',')
    machines = pick_machines(subscribed_resource_groups, subscribed_machines, configured_resource_groups)

    assert len(machines) == 1


def test_pick_machines_with_two_fitting_vm():
    subscribed_resource_groups = [MyResourceGroup(id='1234/res_group_one', name='res_group_one'),
                                  MyResourceGroup(id='9876/res_group_two', name='res_group_two')]
    subscribed_machines = [MyVirtualMachine(id='1234/res_group_one/myvmname'),
                           MyVirtualMachine(id='9876/res_group_two/myvmname')]
    configured_resource_groups = 'res_group_one,res_group_two'.split(',')
    machines = pick_machines(subscribed_resource_groups, subscribed_machines, configured_resource_groups)

    assert len(machines) == 2


def test_pick_machines_with_multiple_vm_but_only_one_vm_fits():
    subscribed_resource_groups = [MyResourceGroup(id='1234/res_group_one', name='res_group_one'),
                                  MyResourceGroup(id='9876/res_group_two', name='res_group_two')]
    subscribed_machines = [MyVirtualMachine(id='1234/res_group_one/myvmname'),
                           MyVirtualMachine(id='5555/res_group_other/myvmname')]
    configured_resource_groups = 'res_group_one,res_group_two'.split(',')
    machines = pick_machines(subscribed_resource_groups, subscribed_machines, configured_resource_groups)

    assert len(machines) == 1


class MyVirtualMachine:

    def __init__(self, id):
        self.id = id


class MyResourceGroup:

    def __init__(self, id, name):
        self.id = id
        self.name = name
