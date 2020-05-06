from abc import ABCMeta, abstractmethod

from chaoslib import Secrets
from chaoslib.exceptions import InterruptExecution
from msrestazure.azure_active_directory import AADMixin, \
    AADTokenCredentials, ServicePrincipalCredentials

from chaosazure.common import cloud


class Auth(metaclass=ABCMeta):

    @abstractmethod
    def create(self, secrets: Secrets) -> AADMixin:
        raise InterruptExecution("Not implemented")


class ServicePrincipalAuth(Auth):

    def create(self, secrets: Secrets) -> ServicePrincipalCredentials:
        _cloud = cloud.get_or_raise(secrets.get('azure_cloud'))
        result = ServicePrincipalCredentials(
            client_id=secrets.get('client_id'),
            secret=secrets.get('client_secret'),
            tenant=secrets.get('tenant_id'),
            cloud_environment=_cloud
        )
        return result


class TokenAuth(Auth):

    def create(self, secrets: Secrets) -> AADTokenCredentials:
        _cloud = cloud.get_or_raise(secrets['azure_cloud'])
        result = AADTokenCredentials(
            {"accessToken": secrets['access_token']},
            secrets['client_id'],
            cloud_environment=_cloud)

        return result
