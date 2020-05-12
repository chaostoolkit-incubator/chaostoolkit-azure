from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

import chaosazure
from chaosazure.vmss.actions import delete_vmss
from chaosazure.vmss.fetcher import fetch_vmss, fetch_instances
from tests.data import vmss_provider


@patch('chaosazure.vmss.fetcher.fetch_resources', autospec=True)
def test_succesful_fetch_vmss(mocked_fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    mocked_fetch_vmss.return_value = scale_sets

    result = fetch_vmss(None, None, None)

    assert len(result) == 1
    assert result[0].get('name') == 'chaos-machine'


@patch('chaosazure.vmss.fetcher.fetch_resources', autospec=True)
def test_empty_fetch_vmss(mocked_fetch_vmss):
    with pytest.raises(FailedActivity) as x:
        mocked_fetch_vmss.return_value = []
        fetch_vmss(None, None, None)

        assert "No VMSS" in str(x.value)


@patch.object(chaosazure.vmss.fetcher, '__fetch_vmss_instances', autospec=True)
def test_succesful_fetch_instances_without_instance_criteria(mocked_fetch_instances):
    instance = vmss_provider.provide_instance()
    instances = [instance]
    mocked_fetch_instances.return_value = instances

    scale_set = vmss_provider.provide_scale_set()

    result = fetch_instances(scale_set, None, None, None)

    assert len(result) == 1
    assert result[0].get('name') == 'chaos-machine'
    assert result[0].get('instanceId') == '0'


@patch.object(chaosazure.vmss.fetcher, '__fetch_vmss_instances', autospec=True)
def test_empty_fetch_instances_without_instance_criteria(mocked_fetch_instances):
    with pytest.raises(FailedActivity) as x:
        mocked_fetch_instances.return_value = []
        scale_set = vmss_provider.provide_scale_set()

        fetch_instances(scale_set, None, None, None)

        assert "No VMSS instances" in str(x.value)


@patch.object(chaosazure.vmss.fetcher, '__fetch_vmss_instances', autospec=True)
def test_succesful_fetch_instances_with_instance_criteria_for_instance0(mocked_fetch_instances):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0['instanceId'] = '0'
    instance_1 = vmss_provider.provide_instance()
    instance_1['instanceId'] = '1'
    instance_2 = vmss_provider.provide_instance()
    instance_2['instanceId'] = '2'
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    result = fetch_instances(scale_set, [{'instanceId': '0'}], None, None)

    # assert
    assert len(result) == 1
    assert result[0].get('name') == 'chaos-machine'
    assert result[0].get('instanceId') == '0'


@patch.object(chaosazure.vmss.fetcher, '__fetch_vmss_instances', autospec=True)
def test_succesful_fetch_instances_with_instance_criteria_for_instance0_instance_2(mocked_fetch_instances):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0['instanceId'] = '0'
    instance_1 = vmss_provider.provide_instance()
    instance_1['instanceId'] = '1'
    instance_2 = vmss_provider.provide_instance()
    instance_2['instanceId'] = '2'
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    result = fetch_instances(scale_set, [{'instanceId': '0'}, {'instanceId': '2'}], None, None)

    # assert
    assert len(result) == 2
    assert result[0].get('name') == 'chaos-machine'
    assert result[0].get('instanceId') == '0'
    assert result[1].get('name') == 'chaos-machine'
    assert result[1].get('instanceId') == '2'


@patch.object(chaosazure.vmss.fetcher, '__fetch_vmss_instances', autospec=True)
def test_succesful_fetch_instances_with_instance_criteria_for_all_instances(mocked_fetch_instances):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0['instanceId'] = '0'
    instance_1 = vmss_provider.provide_instance()
    instance_1['instanceId'] = '1'
    instance_2 = vmss_provider.provide_instance()
    instance_2['instanceId'] = '2'
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    result = fetch_instances(
        scale_set, [{'instanceId': '0'}, {'instanceId': '1'}, {'instanceId': '2'}], None, None)

    # assert
    assert len(result) == 3
    assert result[0].get('name') == 'chaos-machine'
    assert result[0].get('instanceId') == '0'
    assert result[1].get('name') == 'chaos-machine'
    assert result[1].get('instanceId') == '1'
    assert result[2].get('name') == 'chaos-machine'
    assert result[2].get('instanceId') == '2'


@patch.object(chaosazure.vmss.fetcher, '__fetch_vmss_instances', autospec=True)
def test_empty_fetch_instances_with_instance_criteria(mocked_fetch_instances):
    # arrange
    instance_0 = vmss_provider.provide_instance()
    instance_0['instanceId'] = '0'
    instance_1 = vmss_provider.provide_instance()
    instance_1['instanceId'] = '1'
    instance_2 = vmss_provider.provide_instance()
    instance_2['instanceId'] = '2'
    instances = [instance_0, instance_1, instance_2]
    mocked_fetch_instances.return_value = instances
    scale_set = vmss_provider.provide_scale_set()

    # fire
    with pytest.raises(FailedActivity) as x:
        fetch_instances(
            scale_set, [{'instanceId': '99'}, {'instanceId': '100'}, {'instanceId': '101'}], None, None)

        assert "No VMSS instance" in x.value
