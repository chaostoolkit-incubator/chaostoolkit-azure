from chaosazure.machine.constants import RES_TYPE_VM


def provide_machine(os_type: str = "Linux"):
    return {
        "name": "chaos-machine",
        "resourceGroup": "rg",
        "type": RES_TYPE_VM,
        "properties": {"storageProfile": {"osDisk": {"osType": os_type}}},
    }
