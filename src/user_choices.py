class user_choices:
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
        self.attribute_range = []