from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

from chaosazure import auth


def fetch_resources(query, resource_type, secrets, configuration):
    with auth(secrets) as cred:
        query = __create_resource_graph_query(
            query, resource_type, configuration)
        client = ResourceGraphClient(credentials=cred)
        resources = client.resources(query)

        results = __to_dicts(resources.data)
        return results


def __to_dicts(table):
    results = []
    for row in table.rows:
        result = {}
        for col_index in range(len(table.columns)):
            result[table.columns[col_index].name] = row[col_index]
        results.append(result)
    return results


def __create_resource_graph_query(query, resource_type, configuration):
    subscription_id = configuration['azure']['subscription_id']
    _query = __create_query(resource_type, query)
    query = QueryRequest(
        query=_query,
        subscriptions=[subscription_id],
        additional_properties=True
    )
    return query


def __create_query(resource_type, query) -> str:
    where = "where type =~ '{}'".format(resource_type)
    if not query:
        result = "{}".format(where)
    else:
        result = "{}| {}".format(where, query)

    return result
