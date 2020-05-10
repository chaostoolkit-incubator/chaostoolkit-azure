import contextlib
from typing import Dict

from chaoslib.exceptions import InterruptExecution
from msrest.exceptions import AuthenticationError
from msrestazure.azure_active_directory import AADMixin

from chaosazure.auth.authentication import ServicePrincipalAuth, TokenAuth

AAD_TOKEN = "aad_token"
SERVICE_PRINCIPAL = "service_principal"


@contextlib.contextmanager
def auth(secrets: Dict) -> AADMixin:
    """
    Create Azure authentication client from a provided secrets.

    Service principle and token based auth types are supported. Token
    based auth do not currently support refresh token functionality.

    Type of authentication client is determined based on passed secrets.

    For example, secrets that contains a `client_id`, `client_secret` and
    `tenant_id` will create ServicePrincipalAuth client
    ```python
    {
        "client_id": "AZURE_CLIENT_ID",
        "client_secret": "AZURE_CLIENT_SECRET",
        "tenant_id": "AZURE_TENANT_ID"
    }
    ```
    If you are not working with Public Global Azure, e.g. China Cloud
    you can provide `msrestazure.azure_cloud.Cloud` object. If omitted the
    Public Cloud is taken as default. Please refer to msrestazure.azure_cloud
    ```python
    {
        "client_id": "xxxxxxx",
        "client_secret": "*******",
        "tenant_id": "@@@@@@@@@@@",
        "cloud": "msrestazure.azure_cloud.Cloud"
    }
    ```

    If the `client_secret` is not provided, then token based credentials is
    assumed and an `access_token` value must be present in `secrets` object
    and updated when the token expires.
    ```

    Using this function goes as follows:

    ```python
    with auth(secrets) as cred:
        subscription_id = configuration.get("subscription_id")
        resource_client = ResourceManagementClient(cred, subscription_id)
        compute_client = ComputeManagementClient(cred, subscription_id)
    ```

    Again, if you are not working with Public Azure Cloud,
    and you set azure_cloud in secret,
    this will pass one more parameter `base_url` to above function.
    ```python
    with auth(secrets) as cred:
        cloud = cred.get('cloud')
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id,
                        base_url=cloud.endpoints.resource_manager)
    ```

    """

    # No input validation needed:
    # 1) Either no secrets are passed at all - chaostoolkit-lib
    #    will handle it for us *or*
    # 2) Secret arguments are partially missing or invalid - we
    #    rely on the ms azure library
    yield __create(secrets)


##################
# HELPER FUNCTIONS
##################

def __create(secrets: Dict) -> AADMixin:
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


def __authentication_type(secrets: dict) -> str:
    if 'client_secret' in secrets and secrets['client_secret']:
        return SERVICE_PRINCIPAL

    elif 'access_token' in secrets and secrets['access_token']:
        return AAD_TOKEN

    else:
        raise InterruptExecution(
            "Authentication to Azure requires a"
            " client secret or an access token")
