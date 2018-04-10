import sqlite3

class Database:

    def __init__(self, provider=sqlite3, db_name=''):
        self.provider = provider
        self.db_name = db_name

    def get_connection(self):
        return self.provider.connect(self.db_name)



class Query:

    def __init__(self, db_connection):
        self._db_connection = db_connection

    def create_table(self):
        """ CREATE TABLE ... """
        try:
            with self._db_connection:
                self._db_connection.execute('''CREATE TABLE test (date text, trans text, symbol text)''')
        except sqlite3.Error as e:
            print("Unable to create a table. Transaction rolled back. Here is some debug info:", e)
        # cursor = self._db.cursor()
        # cursor.execute('''CREATE TABLE test (date text, trans text, symbol text)''')

    def fetchall(self):
        """ SELECT * FROM ... """
        pass

    def insert(self):
        """ INSERT INTO ... """
        cursor = self._db_connection.cursor()
        cursor.execute('''INSERT INTO test VALUES (?, ?, ?)''', ('2018-04-09', 'Test value', 'Hello'))

    def fix_transaction(self):
        self._db_connection.commit()
        self._db_connection.close()

    def Table(self, tablename):
        pass


# connection = Database(provider=sqlite3, db_name='test_db.sqlite').get_connection()
#
# query = Query(connection)
# query.create_table()
# query.insert()
# query.fix_transaction()
#
# from .v2_models import User
# User(id=1, username='doe', connection=conn).select_all()

        # cursor = conn.cursor()
        # cursor.execute('''CREATE TABLE test (date text, trans text, symbol text)''')
        # cursor.execute('''INSERT INTO test VALUES ('2018-04-09', 'Test value', 'Hello')''')
        # conn.commit()
        # conn.close()
    # query = Query(db).Table('Product').fetchall()
    # print([row for row in query])
