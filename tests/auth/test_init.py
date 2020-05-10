from unittest.mock import patch, MagicMock

import pytest
from chaoslib.exceptions import InterruptExecution
from msrest.exceptions import AuthenticationError
from chaosazure.auth import auth, authentication
from tests.data import secrets_provider


def test_violate_authentication_type():
    secrets = secrets_provider.provide_violating_secrets()

    with pytest.raises(InterruptExecution) as _:
        with auth(secrets) as _:
            pass


@patch.object(authentication.ServicePrincipalAuth, 'create')
def test_create_service_principal_auth(mocked_auth_create):
    mocked_auth_create.return_value = MagicMock()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    with auth(secrets) as _:
        pass

    mocked_auth_create.assert_called_once_with(secrets)


@patch.object(authentication.TokenAuth, 'create')
def test_create_token_auth(mocked_auth_create):
    mocked_auth_create.return_value = MagicMock()
    secrets = secrets_provider.provide_secrets_via_token()

    with auth(secrets) as _:
        pass

    mocked_auth_create.assert_called_once_with(secrets)


@patch.object(authentication.ServicePrincipalAuth, 'create')
def test_create_service_principal_with_auth_error(mocked_auth_create):
    secrets = secrets_provider.provide_secrets_via_service_principal()
    inner_exception = MagicMock()
    mocked_auth_create.side_effect = \
        AuthenticationError("Auth error", inner_exception)

    with pytest.raises(InterruptExecution) as _:
        with auth(secrets) as _:
            pass
