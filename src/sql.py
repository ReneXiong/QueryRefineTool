import psycopg2
import sql_list


class DBObj:
    TIMEOUT = 60

    def __init__(self, addr, port, username, password, dbname):
        self.addr = addr
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.conn = None
        self.cor = None
        self.schema = None
        self.table = None
        self.attribute = []

    def connect(self):
        print("connecting to %s:%s, username: %s, password: %s, dbname = %s" %
              (self.addr, self.port, self.username, self.password, self.dbname))

        try:
            self.conn = psycopg2.connect(
                host=self.addr,
                port=self.port,
                database=self.dbname,
                user=self.username,
                password=self.password,
                connect_timeout=self.TIMEOUT
            )
            self.cor = self.conn.cursor()
        except psycopg2.Error as e:
            raise ConnectionError(e)

        return 0

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cor = None
            print("close connection")
            return 0
        return 1

    def get_cursor(self):
        return self.cor

    def get_attribute(self):
        return self.attribute

    def get_all_schema_names(self):
        sql = sql_list.get_all_schema_sql()
        self.get_cursor().execute(sql)

        result = self.get_cursor().fetchall()
        if (result is None) or (len(result) == 0):
            raise Exception(
                sql_list.get_exception_information("Empty result", sql)
            )

        all_names = []
        for row in result:
            all_names += row
        return all_names

    def get_all_table_names(self, schema_name):
        sql = sql_list.get_all_table_sql(schema_name)
        self.get_cursor().execute(sql)

        result = self.get_cursor().fetchall()
        if (result is None) or (len(result) == 0):
            raise Exception(
                sql_list.get_exception_information("Empty result", sql)
            )

        self.schema = schema_name

        all_names = []
        for row in result:
            all_names += row
        return all_names

    def get_all_int_attributes(self, table_name):
        sql = sql_list.get_all_int_attribute_sql(self.schema, table_name)
        self.get_cursor().execute(sql)

        result = self.get_cursor().fetchall()
        if (result is None) or (len(result) == 0):
            raise Exception(
                sql_list.get_exception_information("Empty result", sql)
            )

        self.table = table_name

        all_names = []
        for row in result:
            if row[1] == "integer":
                all_names.append(row[0])
        return all_names

    def get_current_estimate(self, attribute_name):
        sql = sql_list.get_attribute_range_sql(self.schema, self.table, attribute_name)
        self.get_cursor().execute(sql)

        result = self.get_cursor().fetchall()
        if (result is None) or (len(result) == 0):
            raise Exception(
                sql_list.get_exception_information("Empty result", sql)
            )

        return result




    """ SAVED IN CASE """
    # def get_lists(self, sql):
    #     self.get_cursor().execute(sql)
    #     result = self.get_cursor().fetchall()
    #     if (result is None) or (len(result) == 0):
    #         raise Exception("No result found, or db error occurred. SQL executed: " + sql)
    #     all_names = []
    #     for row in result:
    #         all_names += [row[1]]
    #     return all_names
