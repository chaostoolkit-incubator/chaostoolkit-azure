from logzero import logger
from azure.common.credentials import ServicePrincipalCredentials


def create_from(secrets) -> ServicePrincipalCredentials:
    if secrets is None:
        logger.error("Client can not create credentials from empty secrets")
        raise Exception("Client can not create credentials from empty secrets")

    credentials = ServicePrincipalCredentials(
        client_id=secrets['azure']['client_id'],
        secret=secrets['azure']['client_secret'],
        tenant=secrets['azure']['tenant_id']
    )
    return credentials
