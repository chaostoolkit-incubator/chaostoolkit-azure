from unittest.mock import patch


from chaosazure.aks.probes import (
    count_managed_clusters,
    describe_managed_clusters,
)


resource = {"name": "chaos-managed_cluster", "resourceGroup": "rg"}


@patch("chaosazure.aks.probes.fetch_resources", autospec=True)
def test_count_managed_clusters(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    count = count_managed_clusters(None, None)

    assert count == 1


@patch("chaosazure.aks.probes.fetch_resources", autospec=True)
def test_describe_managed_clusters(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    description = describe_managed_clusters(None, None)

    assert description[0]["name"] == resource["name"]
    assert description[0]["resourceGroup"] == resource["resourceGroup"]
