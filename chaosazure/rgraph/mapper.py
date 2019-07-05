from datetime import datetime


def to_dicts(table, version):
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
