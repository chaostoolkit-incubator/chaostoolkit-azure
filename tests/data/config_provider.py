def provide_default_config():
    return {"azure_subscription_id": "***"}


def provide_config_from_env():
    return {"azure_subscription_id": {"type": "env", "key": "SUBSCRIPTION_ID"}}
