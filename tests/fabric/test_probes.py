# -*- coding: utf-8 -*-
import os.path
from urllib.parse import urlencode

import requests_mock

from chaosazure.fabric.probes import chaos_report

SF_BASE_URL = "https://localhost:19080"

CONFIG = {
    "endpoint": SF_BASE_URL,
    "verify_tls": False
}

SECRETS = {
    "pem_path": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "cert.pem"))
}

def test_chaos_report():
    # we don't match the start/end UTC
    q = urlencode({
        "api-version": "6.0",
        "timeout": 60
    })
    url = "{}/Tools/Chaos/$/Report?{}".format(SF_BASE_URL, q)

    with requests_mock.mock() as m:
        m.get(url, json={})

        result = chaos_report(
            start_time_utc="4 minutes ago", end_time_utc="now",
            configuration=CONFIG, secrets=SECRETS)

        assert m.called
        assert m.call_count == 1

        assert result == {}