from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

import chaosazure
from chaosazure.vmss.fetcher import fetch_vmss, fetch_instances
from tests.data import vmss_provider


@patch("chaosazure.vmss.fetcher.fetch_resources", autospec=True)
def test_succesful_fetch_vmss(mocked_fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    mocked_fetch_vmss.return_value = scale_sets

    result = fetch_vmss(None, None, None)

    assert len(result) == 1
    assert result[0].get("name") == "chaos-pool"


@patch("chaosazure.vmss.fetcher.fetch_resources", autospec=True)
def test_empty_fetch_vmss(mocked_fetch_vmss):
    with pytest.raises(FailedActivity) as x:
        mocked_fetch_vmss.return_value = []
        fetch_vmss(None, None, None)

        assert "No VMSS" in str(x.value)


@patch.object(chaosazure.vmss.fetcher, "__fetch_vmss_instances", autospec=True)
def test_succesful_fetch_instances_without_instance_criteria(
    mocked_fetch_instances,
):
    instance = vmss_provider.provide_instance()
    instances = [instance]
    mocked_fetch_instances.return_value = instances

    scale_set = vmss_provider.provide_scale_set()

    result = fetch_instances(scale_set, None, None, None)

    assert len(result) == 1
    assert result[0].get("name") == "chaos-pool_0"
    assert result[0].get("instance_id") == "0"


@patch.object(chaosazure.vmss.fetcher, "__fetch_vmss_instances", autospec=True)
def test_empty_fetch_instances_without_instance_criteria(
    mocked_fetch_instances,
):
    with pytest.raises(FailedActivity) as x:
        mocked_fetch_instances.return_value = []
        scale_set = vmss_provider.provide_scale_set()

        fetch_instances(scale_set, None, None, None)

        assert "No VMSS instances" in str(x.value)


@patch.object(chaosazure.vmss.fetcher, "__fetch_vmss_instances", autospec=True)
def test_succesful_fetch_instances_with_instance_criteria_for_instance0(
    mocked_fetch_instances,
):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0["instance_id"] = "0"
    instance_1 = vmss_provider.provide_instance()
    instance_1["instance_id"] = "1"
    instance_2 = vmss_provider.provide_instance()
    instance_2["instance_id"] = "2"
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    result = fetch_instances(scale_set, [{"instance_id": "0"}], None, None)

    # assert
    assert len(result) == 1
    assert result[0].get("name") == "chaos-pool_0"
    assert result[0].get("instance_id") == "0"


@patch.object(chaosazure.vmss.fetcher, "__fetch_vmss_instances", autospec=True)
def test_succesful_fetch_instances_with_instance_criteria_for_instance0_instance_2(
    mocked_fetch_instances,
):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0["instance_id"] = "0"
    instance_0["name"] = "chaos-pool_0"
    instance_1 = vmss_provider.provide_instance()
    instance_1["instance_id"] = "1"
    instance_1["name"] = "chaos-pool_1"
    instance_2 = vmss_provider.provide_instance()
    instance_2["instance_id"] = "2"
    instance_2["name"] = "chaos-pool_2"
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    result = fetch_instances(
        scale_set, [{"instance_id": "0"}, {"instance_id": "2"}], None, None
    )

    # assert
    assert len(result) == 2
    assert result[0].get("name") == "chaos-pool_0"
    assert result[0].get("instance_id") == "0"
    assert result[1].get("name") == "chaos-pool_2"
    assert result[1].get("instance_id") == "2"


@patch.object(chaosazure.vmss.fetcher, "__fetch_vmss_instances", autospec=True)
def test_succesful_fetch_instances_with_instance_criteria_for_all_instances(
    mocked_fetch_instances,
):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0["instance_id"] = "0"
    instance_0["name"] = "chaos-pool_0"
    instance_1 = vmss_provider.provide_instance()
    instance_1["instance_id"] = "1"
    instance_1["name"] = "chaos-pool_1"
    instance_2 = vmss_provider.provide_instance()
    instance_2["instance_id"] = "2"
    instance_2["name"] = "chaos-pool_2"
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    result = fetch_instances(
        scale_set,
        [{"instance_id": "0"}, {"instance_id": "1"}, {"instance_id": "2"}],
        None,
        None,
    )

    # assert
    assert len(result) == 3
    assert result[0].get("name") == "chaos-pool_0"
    assert result[0].get("instance_id") == "0"
    assert result[1].get("name") == "chaos-pool_1"
    assert result[1].get("instance_id") == "1"
    assert result[2].get("name") == "chaos-pool_2"
    assert result[2].get("instance_id") == "2"


@patch.object(chaosazure.vmss.fetcher, "__fetch_vmss_instances", autospec=True)
def test_empty_fetch_instances_with_instance_criteria(mocked_fetch_instances):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0["instance_id"] = "0"
    instance_1 = vmss_provider.provide_instance()
    instance_1["instance_id"] = "1"
    instance_2 = vmss_provider.provide_instance()
    instance_2["instance_id"] = "2"
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    with pytest.raises(FailedActivity) as x:
        fetch_instances(
            scale_set,
            [
                {"instance_id": "99"},
                {"instance_id": "100"},
                {"instance_id": "101"},
            ],
            None,
            None,
        )

        assert "No VMSS instance" in x.value
