
class sqlObj:
    def __init__(self, addr, port, dbname, table):
        self.addr = addr
        self.port = port
        self.dbName = dbname
        self.table = table

    def connect(self):
        print("UNDER DEVELOPMENT: connecting to %s:%s, dbName: %s, tableName: %s" %
              (self.addr, self.port, self.dbName, self.table))

        return 0