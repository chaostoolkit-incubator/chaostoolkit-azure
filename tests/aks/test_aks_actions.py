from unittest.mock import MagicMock, patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.aks.actions import (
    restart_node,
    stop_node,
    delete_node,
    start_managed_clusters,
    stop_managed_clusters,
    delete_managed_clusters,
)

resource = {
    "name": "chaos-aks",
    "resourceGroup": "rg",
    "properties": {"nodeResourceGroup": "nrg"},
}

CONFIG = {"azure": {"subscription_id": "***REMOVED***"}}

SECRETS = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
}

SECRETS_CHINA = {
    "client_id": "***REMOVED***",
    "client_secret": "***REMOVED***",
    "tenant_id": "***REMOVED***",
    "azure_cloud": "AZURE_CHINA_CLOUD",
}

MANAGED_CLUSTER_ALPHA = {
    "name": "ManagedClusterAlpha",
    "resourceGroup": "group",
}

MANAGED_CLUSTER_BETA = {"name": "ManagedClusterBeta", "resourceGroup": "group"}


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
@patch("chaosazure.aks.actions.delete_machines", autospec=True)
def test_delete_node(delete, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    delete_node(None, None, None)


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
def test_restart_node_with_no_nodes(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_node(None, None, None)

    assert "No AKS clusters found" in str(x.value)


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
@patch("chaosazure.aks.actions.stop_machines", autospec=True)
def test_stop_node(stop, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    stop_node(None, None, None)


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
@patch("chaosazure.aks.actions.restart_machines", autospec=True)
def test_restart_node(restart, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    restart_node(None, None, None)


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_delete_one_managed_cluster(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_managed_clusters(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.managed_clusters.begin_delete.call_count == 1


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_delete_one_MANAGED_CLUSTER_china(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_managed_clusters(f, CONFIG, SECRETS_CHINA)

    fetch.assert_called_with(f, CONFIG, SECRETS_CHINA)
    assert client.managed_clusters.begin_delete.call_count == 1


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_delete_two_managed_clusters(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA, MANAGED_CLUSTER_BETA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_managed_clusters(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.managed_clusters.begin_delete.call_count == 2


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
def test_delete_MANAGED_CLUSTER_with_no_managed_clusters(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_managed_clusters(None, None, None)

    assert "No Managed Clusters found" in str(x.value)


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_start_one_managed_cluster(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    start_managed_clusters(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.managed_clusters.begin_start.call_count == 1


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_start_two_managed_clusters(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA, MANAGED_CLUSTER_BETA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    start_managed_clusters(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.managed_clusters.begin_start.call_count == 2


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
def test_start_MANAGED_CLUSTER_with_no_managed_clusters(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        start_managed_clusters(None, None, None)

    assert "No Managed Clusters found" in str(x.value)


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_stop_one_managed_cluster(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_managed_clusters(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.managed_clusters.begin_stop.call_count == 1


@patch("chaosazure.aks.actions.__fetch_managed_clusters", autospec=True)
@patch("chaosazure.aks.actions.__containerservice_mgmt_client", autospec=True)
def test_stop_two_managed_clusters(init, fetch):
    client = MagicMock()
    init.return_value = client

    managed_clusters = [MANAGED_CLUSTER_ALPHA, MANAGED_CLUSTER_BETA]
    fetch.return_value = managed_clusters

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_managed_clusters(f, CONFIG, SECRETS)

    fetch.assert_called_with(f, CONFIG, SECRETS)
    assert client.managed_clusters.begin_stop.call_count == 2


@patch("chaosazure.aks.actions.fetch_resources", autospec=True)
def test_stop_MANAGED_CLUSTER_with_no_managed_clusters(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_managed_clusters(None, None, None)

    assert "No Managed Clusters found" in str(x.value)
