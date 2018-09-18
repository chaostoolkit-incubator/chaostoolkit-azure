# -*- coding: utf-8 -*-
import json
import os.path

from chaoslib.exceptions import FailedActivity
import pytest
import requests
import requests_mock

from chaosazure.fabric.actions import start_chaos, stop_chaos

SF_BASE_URL = "https://localhost:19080"

CONFIG = {
    "endpoint": SF_BASE_URL,
    "verify_tls": False
}

SECRETS = {
    "pem_path": os.path.abspath(
        os.path.join(os.path.dirname(__file__), "cert.pem"))
}

CHAOS_PARAMS = {
    "TimeToRunInSeconds": 30,
    "ClusterHealthPolicy": {
        "ConsiderWarningAsError": True
    }
}

def test_start_chaos():
    url = "{}/Tools/Chaos/$/Start?api-version=6.0&timeout=60".format(
        SF_BASE_URL)

    with requests_mock.mock() as m:
        m.post(url, complete_qs=True, json=["started!"])

        result = start_chaos(
            CHAOS_PARAMS, configuration=CONFIG, secrets=SECRETS)

        assert m.called
        assert m.call_count == 1

        assert result == ["started!"]


def test_stop_chaos():
    url = "{}/Tools/Chaos/$/Stop?api-version=6.0&timeout=60".format(
        SF_BASE_URL)

    with requests_mock.mock() as m:
        m.post(url, complete_qs=True, json=["stopped!"])

        result = stop_chaos(configuration=CONFIG, secrets=SECRETS)

        assert m.called
        assert m.call_count == 1

        assert result == ["stopped!"]


def test_start_chaos_fails_when_missing_config_path_and_endpoint():
    url = "{}/Tools/Chaos/$/Start?api-version=6.0&timeout=60".format(
        SF_BASE_URL)

    with requests_mock.mock() as m:
        m.post(url, complete_qs=True, json=["started!"])

        with pytest.raises(FailedActivity) as x:
            start_chaos(CHAOS_PARAMS)

        assert m.called is False
        assert m.call_count == 0
        assert "client needs to know how to authenticate" in str(x)


def test_start_chaos_using_local_config_file():
    url = "{}/Tools/Chaos/$/Start?api-version=6.0&timeout=60".format(
        SF_BASE_URL)

    with requests_mock.mock() as m:
        m.post(url, complete_qs=True, json=["started!"])

        result = start_chaos(CHAOS_PARAMS, configuration={
            "config_path": os.path.join(
                os.path.dirname(__file__), "vmconfig")
        })

        assert m.called
        assert m.call_count == 1
        assert result == ["started!"]


def test_start_chaos_filas_when_local_config_file_not_found():
    url = "{}/Tools/Chaos/$/Start?api-version=6.0&timeout=60".format(
        SF_BASE_URL)

    with requests_mock.mock() as m:
        m.post(url, complete_qs=True, json=["started!"])

        with pytest.raises(FailedActivity) as x:
            start_chaos(
                CHAOS_PARAMS, configuration={"config_path": "whatever"})

        assert m.called is False
        assert m.call_count == 0
        assert "Service Fabric configuration file not found at" in str(x)


def test_start_chaos_can_fail():
    url = "{}/Tools/Chaos/$/Start?api-version=6.0&timeout=60".format(
        SF_BASE_URL)

    with requests_mock.mock() as m:
        m.post(url, complete_qs=True, json={
            "Error": {
                "Code": "FABRIC_E_INVALID_CONFIGURATION",
                "Message": "boom"
            }
        }, status_code=400)

        with pytest.raises(FailedActivity) as x:
            start_chaos(CHAOS_PARAMS, configuration=CONFIG, secrets=SECRETS)

        assert m.called is True
        assert m.call_count == 1

        assert "Service Fabric Chaos failed to start" in str(x)
