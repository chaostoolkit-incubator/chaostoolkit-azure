from chaosazure.vmss.constants import RES_TYPE_VMSS_VM, RES_TYPE_VMSS


def provide_instance():
    return {
        "name": "chaos-pool_0",
        "instance_id": "0",
        "type": RES_TYPE_VMSS_VM,
    }


def provide_scale_set():
    return {
        "name": "chaos-pool",
        "resourceGroup": "rg",
        "type": RES_TYPE_VMSS,
    }
