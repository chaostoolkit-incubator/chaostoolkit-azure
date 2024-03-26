from chaosazure.postgresql.constants import RES_TYPE_SRV_PG


def provide_database():
    return {
        "name": "chaos-database",
        "resourceGroup": "rg",
        "type": RES_TYPE_SRV_PG,
        "properties": {"version": "11", "storageProfile": {"storageMB": 5120}},
    }
