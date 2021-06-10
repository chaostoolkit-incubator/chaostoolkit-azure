from abc import ABCMeta, abstractmethod
from typing import Dict

from chaoslib import Secrets
from chaoslib.exceptions import InterruptExecution
from msrestazure.azure_active_directory import AADMixin, AADTokenCredentials
from azure.identity import ClientSecretCredential


class Auth(metaclass=ABCMeta):

    @abstractmethod
    def create(self, secrets: Secrets) -> AADMixin:
        raise InterruptExecution("Not implemented")


class ServicePrincipalAuth(Auth):

    def create(self, secrets: Dict) -> ClientSecretCredential:
        result = ClientSecretCredential(
            client_id=secrets.get('client_id'),
            client_secret=secrets.get('client_secret'),
            tenant_id=secrets.get('tenant_id'),
            cloud_environment=secrets.get('cloud')
        )
        return result


class TokenAuth(Auth):

    def create(self, secrets: Dict) -> AADTokenCredentials:
        result = AADTokenCredentials(
            token={"accessToken": secrets['access_token']},
            client_id=secrets.get('client_id'),
            cloud_environment=secrets.get('cloud'))

        return result
