from chaosazure.netapp.constants import RES_TYPE_SRV_NV


def provide_netapp_volume():
    return {
        "name": "chaos-netapp-account/chaos-pool/chaos-volume",
        "resourceGroup": "rg",
        "type": RES_TYPE_SRV_NV,
    }
