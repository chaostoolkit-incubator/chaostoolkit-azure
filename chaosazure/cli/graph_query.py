from typing import List


def filter_type_command(resource_type, filter) -> List[str]:
    where = "where type =~ '{}'".format(resource_type)
    if not filter:
        command = ['graph', 'query', '-q', "{}".format(where)]
    else:
        command = ['graph', 'query', '-q', "{}| {}".format(where, filter)]

    return command
