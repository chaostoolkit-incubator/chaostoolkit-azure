from chaosazure.storage.constants import RES_TYPE_SRV_SA


def provide_storage_account():
    return {
        "name": "chaos-storage-account",
        "resourceGroup": "rg",
        "type": RES_TYPE_SRV_SA,
    }
