from chaosazure.cli.graph_query import filter_type_command

TESTED_RESOURCE = "Microsoft.ContainerService/managedClusters"


def test_full_graph_query():
    test_filter = "where name =~'my-resource-name'"
    command = filter_type_command(TESTED_RESOURCE,
                                  test_filter)

    assert len(command) == 4
    assert command[3] == "where type =~ '{}'| {}".format(TESTED_RESOURCE,
                                                         test_filter)


def test_graph_query_without_filter_none_string():
    command = filter_type_command(TESTED_RESOURCE, None)

    assert len(command) == 4
    assert command[3] == "where type =~ '{}'".format(TESTED_RESOURCE)


def test_graph_query_without_filter_empty_string():
    command = filter_type_command(TESTED_RESOURCE, "")

    assert len(command) == 4
    assert command[3] == "where type =~ '{}'".format(TESTED_RESOURCE)
