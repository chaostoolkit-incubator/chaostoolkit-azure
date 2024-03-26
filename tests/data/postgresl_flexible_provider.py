from chaosazure.postgresql_flexible.constants import RES_TYPE_SRV_PG_FLEX


def provide_database():
    return {
        "name": "chaos-database",
        "resourceGroup": "rg",
        "type": RES_TYPE_SRV_PG_FLEX,
        "properties": {"version": "13", "storage": {"storageSizeGB": 32}},
    }
