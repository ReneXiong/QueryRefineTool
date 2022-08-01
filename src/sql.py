import psycopg2


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

    def get_all_table_names(self):

        self.get_cursor().execute("""SELECT * FROM pg_catalog.pg_tables
        WHERE schemaname = 'public';""")
        result = self.get_cursor().fetchall()
        if (result is None) or (len(result) == 0):
            raise Exception("No table found, or db error occurred")
        all_names = []
        for row in result:
            all_names += [row[1]]
        return all_names
