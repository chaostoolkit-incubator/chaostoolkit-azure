from unittest.mock import patch

from chaosazure.machine.probes import count_machines, describe_machines

resource = {"name": "chaos-machine", "resourceGroup": "rg"}


@patch("chaosazure.machine.probes.fetch_resources", autospec=True)
def test_count_machines(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    count = count_machines(None, None)

    assert count == 1


@patch("chaosazure.machine.probes.fetch_resources", autospec=True)
def test_describe_machines(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    description = describe_machines(None, None)

    assert description[0]["name"] == resource["name"]
    assert description[0]["resourceGroup"] == resource["resourceGroup"]
