from chaoslib import Secrets
from chaoslib.exceptions import InterruptExecution
from msrest.exceptions import AuthenticationError
from msrestazure.azure_active_directory import AADMixin

from chaosazure.auth.authentication import Auth, \
    ServicePrincipalAuth, TokenAuth

AAD_TOKEN = "aad_token"
SERVICE_PRINCIPAL = "service_principal"


def create(secrets: Secrets) -> AADMixin:
    _auth_type = __authentication_type(secrets)

    if _auth_type == SERVICE_PRINCIPAL:
        _authentication = ServicePrincipalAuth()

    elif _auth_type == AAD_TOKEN:
        _authentication = TokenAuth()

    try:
        result = _authentication.create(secrets)
        return result
    except AuthenticationError as e:
        msg = e.inner_exception.error_response.get('error_description')
        raise InterruptExecution(msg)


##################
# HELPER FUNCTIONS
##################

def __authentication_type(secrets: dict) -> str:
    if 'client_secret' in secrets and secrets['client_secret']:
        return SERVICE_PRINCIPAL

    elif 'access_token' in secrets and secrets['access_token']:
        return AAD_TOKEN

    else:
        raise InterruptExecution(
            "Authentication to Azure requires a"
            " client secret or an access token")
