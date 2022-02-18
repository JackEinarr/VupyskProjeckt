import psycopg2
from psycopg2 import connect

class On_bd():
    def __init__(self, *arg, **kwarg):

        self.bdname = "test_v"
        self.user = "postgres"
        self.password = "1"
        self.host = "127.0.0.1"

        self.conn = connect(dbname=self.bdname, user=self.user,
                        password=self.password, host=self.host)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def Unconnect(self):
        self.cursor.close()
        self.conn.close()