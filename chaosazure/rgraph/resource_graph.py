from datetime import datetime

from azure.mgmt.resourcegraph.models \
    import QueryRequest, ErrorResponseException
from chaoslib.exceptions import InterruptExecution
from logzero import logger

from chaosazure import init_resource_graph_client


def fetch_resources(input_query: str, resource_type: str,
                    secrets, configuration):
    # prepare query
    _query = __query_from(resource_type, input_query)
    _query_request = __query_request_from(_query, configuration)

    # prepare resource graph client
    try:
        client = init_resource_graph_client(secrets)
        resources = client.resources(_query_request)
    except ErrorResponseException as e:
        msg = e.inner_exception.error.code
        if e.inner_exception.error.details:
            for d in e.inner_exception.error.details:
                msg += ": " + str(d)
        logger.error(msg)
        raise InterruptExecution(msg)

    # prepare results
    results = __to_dicts(resources.data, client.api_version)
    return results


def __query_request_from(query, configuration):
    subscription_id = configuration.get("azure_subscription_id")
    if not subscription_id:
        subscription_id = configuration['azure']['subscription_id']

    result = QueryRequest(
        query=query,
        subscriptions=[subscription_id]
    )
    return result


def __query_from(resource_type, query) -> str:
    where = "where type=~'{}'".format(resource_type)
    if not query:
        result = "{}".format(where)
    else:
        result = "{}| {}".format(where, query)

    return "Resources | {}".format(result)


def __to_dicts(table, version):
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
