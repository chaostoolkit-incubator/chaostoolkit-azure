from unittest.mock import MagicMock, patch


from chaosazure.postgresql.probes import (
    count_servers,
    describe_servers,
    describe_databases,
)
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Database

resource = {"name": "chaos-server", "resourceGroup": "rg"}

database_resource = Database(charset="UTF8")
database_resource.name = "chaos-db"


@patch("chaosazure.postgresql.probes.fetch_resources", autospec=True)
def test_count_servers(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    count = count_servers(None, None)

    assert count == 1


@patch("chaosazure.postgresql.probes.fetch_resources", autospec=True)
def test_describe_servers(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    description = describe_servers(None, None)

    assert description[0]["name"] == resource["name"]
    assert description[0]["resourceGroup"] == resource["resourceGroup"]


@patch("chaosazure.postgresql.probes.fetch_resources", autospec=True)
@patch("chaosazure.postgresql.probes.__postgresql_mgmt_client", autospec=True)
def test_describe_databases(init, fetch):
    client = MagicMock()
    init.return_value = client

    client.databases.list_by_server.return_value = [database_resource]

    resource_list = [resource]
    fetch.return_value = resource_list

    description = describe_databases(None, None)

    assert description[0]["name"] == database_resource.name
    assert description[0]["charset"] == database_resource.charset
