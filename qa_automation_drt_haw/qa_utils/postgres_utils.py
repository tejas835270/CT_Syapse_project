
import psycopg2
from qa_automation_drt_haw.ui.ui_utils.Logs import log


class Postgres:
    def __init__(self, host, port, user, password, dbname):
        """
        This is just the constructor of the class which defines the list
        of items required for creating a postgres DB connection.
        """
        connection_details = {
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "database": dbname
        }
        self.create_connection(**connection_details)

    def create_connection(self, **kwargs):
        """
        This function creates the connection to the postgres database
        using the values passed.
        """
        try:
            self.connection = psycopg2.connect(**kwargs)
        except (Exception, psycopg2.DatabaseError) as error:
            log.debug(f"Unable to connect to database. \nError:{error}")
            raise

    def get_query_response_count(self, sql_query):
        """
        This function executes the query and returns the result and row count for the query.
        """
        try:
            log.debug("Executing query : {}".format(sql_query))
            cur = self.connection.cursor()
            cur.execute(sql_query)

            header = [[desc[0] for desc in cur.description]]
            data = header + [list(row) for row in cur.fetchall()]

            cur.close()
            return data, len(data) - 1
        except psycopg2.Error:
            log.error("Unable to execute query")
            raise

    def get_query_response_dict_format(self,sql_query,max_result_count=10):
        '''
        Purpose: This method fetches the response from database and coverts the response format into dictionary format.
        :param sql_query: query for which response is required.
        :param max_result_count: From the fetched result for the query, the count of records will get returned will be equal to "max_result_count"
        :return: Database record set in dictionary format
        :note: Following format will be provided as - result = [{"col1":"val1row1","col2:"val2row1","col3":"val3row1"},{"col1":"val1row2","col2:"val2row2","col3":"val3row2"}] and so on
        '''

        # Fetching the response for the given query. Response is returned as tuple having list of records and count of records
        res = self.get_query_response_count(sql_query)

        # Declaring empty list and dictionary element
        data_list = []
        data_dict = {}

        # Fetching count of records retrieved
        row_count = res[1]

        # Checking if any records are retrieved for given query
        if row_count > 0:

            # We are limiting the record options to 10. (if required it can be increased using max_result_count)
            if row_count > max_result_count:
                row_count = max_result_count

            # Getting table column names retrieved based on query
            headers = res[0][0]

            # Logic to create of list of dictionary values. Each dictionary would have key as column name and value as field value.
            # Different elements in list will be corresponding to the records retrieved for the query.
            for num in range(row_count):
                field_count = len(res[0][num + 1])
                for num_count in range(field_count):
                    data_dict[headers[num_count]] = res[0][num + 1][num_count]

                # Adding created dictionary element into the list
                data_list.append(data_dict.copy())

            return data_list
        else:
            print("No output for given query - %s" % sql_query)
            log.error("No output for given query - %s" % sql_query)

    def __del__(self):
        """
        Destructor to close the DB connection at the end of execution.
        """
        self.connection.close()
