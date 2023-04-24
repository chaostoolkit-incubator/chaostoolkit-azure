def machine(resource: dict) -> dict:
    """
    Free the virtual machine dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties"
    ]

    return __cleanse(cleanse, resource)


def database_server(resource: dict) -> dict:
    """
    Free the database server dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties"
    ]

    return __cleanse(cleanse, resource)


def database_database(resource: dict) -> dict:
    """
    Free the database dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties"
    ]

    return __cleanse(cleanse, resource)


def application_gateway(resource: dict) -> dict:
    """
    Free the database dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties"
    ]

    return __cleanse(cleanse, resource)


def netapp_volume(resource: dict) -> dict:
    """
    Free the database dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties", "tags", "managedBy", "sku", "identity",
        "performed_at", "kind", "plan", "performed_at",
        "extendedLocation"
    ]

    return __cleanse(cleanse, resource)


def managed_cluster(resource: dict) -> dict:
    """
    Free the database dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties", "tags", "managedBy", "sku", "identity",
        "performed_at", "kind", "plan", "performed_at",
        "extendedLocation"
    ]

    return __cleanse(cleanse, resource)


def storage_account(resource: dict) -> dict:
    """
    Free the database dictionary from unwanted keys listed below.
    """
    cleanse = [
        "properties", "tags", "managedBy", "sku", "identity",
        "performed_at", "kind", "plan", "performed_at",
        "extendedLocation"
    ]

    return __cleanse(cleanse, resource)


def blob_storage(resource: dict) -> dict:
    """
    Free the database dictionary from unwanted keys listed below.
    """
    cleanse = [
        "immutable_storage_with_versioning", "enable_nfs_v3_all_squash",
        "enable_nfs_v3_root_squash", "additional_properties"
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
