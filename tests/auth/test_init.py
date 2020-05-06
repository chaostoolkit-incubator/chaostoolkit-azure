from unittest.mock import patch, MagicMock

import pytest
from chaoslib.exceptions import InterruptExecution

from chaosazure.auth import create, authentication
from tests.data import secrets_provider


def test_violate_authentication_type():
    secrets = secrets_provider.provide_violating_secrets()

    with pytest.raises(InterruptExecution) as exception:
        create(secrets)


@patch.object(authentication.ServicePrincipalAuth, 'create')
def test_create_service_principal(mocked_auth_create):
    mocked_auth_create.return_value = MagicMock()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    create(secrets)

    mocked_auth_create.assert_called_once_with(secrets)


@patch.object(authentication.TokenAuth, 'create')
def test_create_service_principal(mocked_auth_create):
    mocked_auth_create.return_value = MagicMock()
    secrets = secrets_provider.provide_secrets_via_token()

    create(secrets)

    mocked_auth_create.assert_called_once_with(secrets)


def test_create_service_principal():
    secrets = secrets_provider.provide_secrets_via_service_principal()

    with pytest.raises(InterruptExecution) as exception:
        create(secrets)
