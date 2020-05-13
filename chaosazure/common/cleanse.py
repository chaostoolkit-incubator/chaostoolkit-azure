def machine(resource: dict) -> dict:
    """
    Free the virtual machine dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties"
    ]

    return __cleanse(cleanse, resource)


def vmss(resource: dict) -> dict:
    """
    Free the VMSS dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties", "instances"
    ]

    return __cleanse(cleanse, resource)


def vmss_instance(resource: dict) -> dict:
    """
    Free the VMSS instance from unwanted keys listed below.
    """
    cleanse = [
        "hardware_profile", "storage_profile", "network_profile",
        "os_profile", "network_profile_configuration", "resources"
    ]

    return __cleanse(cleanse, resource)


def __cleanse(cleanse_list: [], resource: dict) -> dict:
    for key in cleanse_list:
        if key in resource:
            del resource[key]

    return resource
