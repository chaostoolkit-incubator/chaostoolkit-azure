from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

from chaosazure.aks.actions import restart_node, stop_node, delete_node, format_query

resource = {
    'name': 'chaos-aks',
    'resourceGroup': 'rg',
    'properties': {
        'nodeResourceGroup': 'nrg'
    }}


@patch('chaosazure.aks.actions.fetch_resources', autospec=True)
@patch('chaosazure.aks.actions.delete_machines', autospec=True)
def test_delete_node(delete, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    delete_node(None, None, None, None)


@patch('chaosazure.aks.actions.fetch_resources', autospec=True)
def test_restart_node_with_no_nodes(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        delete_node(None, None, None, None)

    assert "No AKS clusters found" in str(x.value)


@patch('chaosazure.aks.actions.fetch_resources', autospec=True)
@patch('chaosazure.aks.actions.stop_machines', autospec=True)
def test_stop_node(stop, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    stop_node(None, None, None, None)


@patch('chaosazure.aks.actions.fetch_resources', autospec=True)
def test_restart_node_with_no_nodes(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        stop_node(None, None, None, None)

    assert "No AKS clusters found" in str(x.value)


@patch('chaosazure.aks.actions.fetch_resources', autospec=True)
@patch('chaosazure.aks.actions.restart_machines', autospec=True)
def test_restart_node(restart, fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    restart_node(None, None, None, None)


@patch('chaosazure.aks.actions.fetch_resources', autospec=True)
def test_restart_node_with_no_nodes(fetch):
    with pytest.raises(FailedActivity) as x:
        resource_list = []
        fetch.return_value = resource_list
        restart_node(None, None, None, None)

    assert "No AKS clusters found" in str(x.value)


def test_format_query():
    query = format_query(1, resource['properties']['nodeResourceGroup'])
    assert query == "where resourceGroup =~ 'nrg' | sample 1"


def test_no_sample_format_query():
    query = format_query(None, resource['properties']['nodeResourceGroup'])
    assert query == "where resourceGroup =~ 'nrg'"

