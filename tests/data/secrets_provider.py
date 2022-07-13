

def provide_secrets_via_service_principal():
    return {
        "client_id": "***",
        "client_secret": "***",
        "tenant_id": "***"
    }


def provide_secrets_germany_small_letters():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = "azure_german_cloud"
    return result


def provide_secrets_via_token():
    return {
        "access_token": "***",
        "client_id": "***",
        "tenant_id": "***",
    }


def provide_secrets_invalid_cloud():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = "this_cloud_does_not_exist"
    return result


def provide_violating_secrets():
    return {
        "client_id": "***",
        "tenant_id": "***",
    }