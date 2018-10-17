# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import json
from typing import Any, Dict

import dateparser
from logzero import logger
import requests

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets

from chaosazure import sf_auth

__all__ = ["chaos_report"]


def chaos_report(timeout: int = 60, start_time_utc: str = None,
                 end_time_utc: str = None, configuration: Configuration = None,
                 secrets: Secrets = None) -> Dict[str, Any]:
    """
    Get Chaos report using following the Service Fabric API:

    https://docs.microsoft.com/en-us/rest/api/servicefabric/sfclient-v60-model-chaosparameters

    Please see the :func:`chaosazure.fabric.auth` help for more information
    on authenticating with the service.
    """  # noqa: E501
    with sf_auth(configuration, secrets) as info:
        url = "{}/Tools/Chaos/$/Report".format(info["endpoint"])

        qs = {"api-version": "6.0"}
        if timeout is not None:
            qs["timeout"] = timeout
        if start_time_utc is not None:
            qs["StartTimeUtc"] = datetime_to_ticks(start_time_utc)
        if end_time_utc is not None:
            qs["EndTimeUtc"] = datetime_to_ticks(end_time_utc)

        r = requests.get(
            url, headers={"Accept": "application/json"},
            verify=info["verify"], params=qs)

        if r.status_code != 200:
            error = r.json()
            raise FailedActivity(
                "Service Fabric Chaos failed to get report: {}".format(
                    json.dumps(error)))

        logger.debug("chaos report fetched succesfully")

        return r.json()


def datetime_to_ticks(when: str) -> int:
    """
    Computes the number of ticks until the relative time given.

    ```python
    >>> datetime_to_ticks("2 mns ago")
    ```
    """
    dt = dateparser.parse(when, settings={'RETURN_AS_TIMEZONE_AWARE': True})
    if not dt:
        raise FailedActivity("failed parsing moment: {}".format(when))

    span = dt - datetime(1, 1, 1, tzinfo=timezone.utc)
    return int(span.total_seconds() * 10**7)
