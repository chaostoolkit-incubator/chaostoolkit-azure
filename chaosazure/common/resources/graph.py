from datetime import datetime
from typing import List

from azure.core.exceptions import HttpResponseError
from azure.mgmt.resourcegraph.models import QueryRequest
from chaoslib.exceptions import InterruptExecution
from chaoslib.types import Secrets, Configuration
from logzero import logger

from chaosazure import init_resource_graph_client
from chaosazure.common.config import load_configuration


def fetch_resources(input_query: str, resource_type: str,
                    secrets: Secrets, configuration: Configuration):
    # prepare query
    _query = __query_from(resource_type, input_query)
    _query_request = __query_request_from(_query, configuration)

    # prepare resource graph client
    try:
        client = init_resource_graph_client(secrets)
        resources = client.resources(_query_request)
    except HttpResponseError as e:
        msg = e.error.code
        if e.error.details:
            for d in e.error.details:
                msg += ": " + str(d)
        raise InterruptExecution(msg)

    # prepare results
    results = __to_dicts(resources.data, client.api_version)
    return results


def __query_request_from(query, experiment_configuration: Configuration):
    configuration = load_configuration(experiment_configuration)
    result = QueryRequest(
        query=query,
        subscriptions=[configuration.get('subscription_id')]
    )
    return result


def __query_from(resource_type, query) -> str:
    where = "where type=~'{}'".format(resource_type)
    if not query:
        result = "{}".format(where)
    else:
        result = "{}| {}".format(where, query)

    return "Resources | {}".format(result)


def __to_dicts(table, version) -> List[dict]:
    results = []
    version_date = datetime.strptime(version, '%Y-%m-%d').date()

    if version_date >= datetime.strptime('2019-04-01', '%Y-%m-%d').date():
        for row in table['rows']:
            result = {}
            for col_index in range(len(table['columns'])):
                result[table['columns'][col_index]['name']] = row[col_index]
            results.append(result)

    else:
        for row in table.rows:
            result = {}
            for col_index in range(len(table.columns)):
                result[table.columns[col_index].name] = row[col_index]
            results.append(result)

    return results
