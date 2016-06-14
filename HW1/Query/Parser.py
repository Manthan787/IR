import re
from Decorators import tokenize, dependency_parse

# "/Users/admin/Documents/CS6200/HW1/AP_DATA/query_desc.51-100.short.txt"
queries_file = "/Users/admin/Documents/CS6200/AP_DATA/queries.short.txt"


@tokenize
def get_queries(query_file):
    """ Returns the queries parsed from the given query file path

        Note: The query file should be in the following format
              <queryNo> <dot> <queryText>

        Args:
            query_file (string): path of the txt file containing the queries

        Returns:
            dict: with <queryNo> as the key and <queryText> as the value
    """
    print "Processing queries form the query file ...."
    with open(query_file, 'r') as f:
        queries = dict()
        for query in f.readlines():
            regex = re.compile(r'^([0-9]+\.)(.*?)$')
            result = regex.findall(query)
            if len(result) > 0:
                queryNo = result[0][0].strip()[:-1]
                queryText = result[0][1].strip()
                queries[queryNo] = queryText

        return queries


if __name__ == "__main__":
    print get_queries(queries_file)
