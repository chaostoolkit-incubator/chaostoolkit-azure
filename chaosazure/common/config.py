
import io
import json
import os

from chaoslib.types import Configuration, Secrets
from logzero import logger
from msrestazure import azure_cloud

from chaosazure.common import cloud


def load_secrets(experiment_secrets: Secrets):
    """Load secrets from experiments or azure credential file.

    :param experiment_secrets: Secrets provided in experiment file
    :returns: a secret object

    Load secrets from multiple sources that can contain different format
    such as azure credential file or experiment secrets section.
    The latter takes precedence over azure credential file.

    Function returns following dictionary object:
    ```python
    {
        # always available
        "cloud": "variable contains msrest cloud object"

        # optional - available if user authenticate with service principal
        "client_id": "variable contains client id",
        "client_secret": "variable contains client secret",
        "tenant_id": "variable contains tenant id",

        # optional - available if user authenticate with existing token
        "access_token": "variable contains access token",
    }
    ```

    :Loading secrets from experiment file:

    Function will try to load following secrets from the experiment file:
    ```json
    {
        "azure": {
            "client_id": "AZURE_CLIENT_ID",
            "client_secret": "AZURE_CLIENT_SECRET",
            "tenant_id": "AZURE_TENANT_ID",
            "access_token": "AZURE_ACCESS_TOKEN"
        }
    }
    ```

    :Loading secrets from azure credential file:

    If experiment file contains no secrets, function will try to load secrets
    from the azure credential file. Path to the file should be set under
    AZURE_AUTH_LOCATION environment variable.

    Function will try to load following secrets from azure credential file:
    ```json
    {
        "clientId": "AZURE_CLIENT_ID",
        "clientSecret": "AZURE_CLIENT_SECRET",
        "tenantId": "AZURE_TENANT_ID",
        "resourceManagerEndpointUrl": "AZURE_RESOURCE_MANAGER_ENDPOINT",
        ...
    }
    ```
    More info about azure credential file may be found:
    https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate

    """

    # 1: lookup for secrets in experiment  file
    if experiment_secrets:
        return {
            'client_id': experiment_secrets.get('client_id'),
            'client_secret': experiment_secrets.get('client_secret'),
            'tenant_id': experiment_secrets.get('tenant_id'),
            # load cloud object
            'cloud': cloud.get_or_raise(experiment_secrets.get('azure_cloud')),
            'access_token': experiment_secrets.get('access_token'),
        }

    # 2: lookup for credentials in azure auth file
    az_auth_file = _load_azure_auth_file()
    if az_auth_file:
        rm_endpoint = az_auth_file.get('resourceManagerEndpointUrl')
        return {
            'client_id': az_auth_file.get('clientId'),
            'client_secret': az_auth_file.get('clientSecret'),
            'tenant_id': az_auth_file.get('tenantId'),
            # load cloud object
            'cloud': azure_cloud.get_cloud_from_metadata_endpoint(rm_endpoint),
            # access token is not supported for credential files
            'access_token': None,
        }

    # no secretes
    logger.warn("Unable to load Azure credentials.")
    return {}


def load_configuration(experiment_configuration: Configuration):
    subscription_id = None
    # 1: lookup for configuration in experiment config file
    if experiment_configuration:
        subscription_id = experiment_configuration.get("azure_subscription_id")
        # check legacy subscription location
        if not subscription_id:
            subscription_id = experiment_configuration\
                .get('azure', {}).get('subscription_id')

    if subscription_id:
        return {'subscription_id': subscription_id}

    # 2: lookup for configuration in azure auth file
    az_auth_file = _load_azure_auth_file()
    if az_auth_file:
        return {'subscription_id': az_auth_file.get('subscriptionId')}

    # no configuration
    logger.warn("Unable to load subscription id.")
    return {}


def _load_azure_auth_file():
    auth_path = os.environ.get('AZURE_AUTH_LOCATION')
    credential_file = {}
    if auth_path and os.path.exists(auth_path):
        with io.open(auth_path, 'r', encoding='utf-8-sig') as auth_fd:
            credential_file = json.load(auth_fd)
    return credential_file
