from unittest.mock import patch

from chaosazure.vmss.probes import count_instances

resource = {"name": "vmss_instance_0", "resourceGroup": "group"}


@patch("chaosazure.vmss.probes.fetch_resources", autospec=True)
def test_count_instances(fetch):
    fetch.return_value = [resource]

    count = count_instances(None, None)

    assert count == 1
