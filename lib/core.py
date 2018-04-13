import sqlite3


class Database:

    def __init__(self, provider=sqlite3, db_name=''):
        self.provider = provider
        self.db_name = db_name

    def get_connection(self):
        return self.provider.connect(self.db_name)


class Query:

    def __init__(self, db_connection, table_name):
        self._db_connection = db_connection
        self.table_name = table_name

    def create_table(self, table_schema):
        """ CREATE TABLE ... """
        try:
            with self._db_connection:
                self._db_connection.execute('CREATE TABLE %s (%s);' % (self.table_name, ', '.join(table_schema)))
        except sqlite3.Error as e:
            print("Unable to create a table. Transaction rolled back. Here is some debug info:", e)

    def fetchall(self, columns):
        """ SELECT * FROM table ... """
        return self._db_connection.execute(
            'SELECT %s FROM %s;' % (', '.join(columns), self.table_name))

    def insert(self, **data):
        """ INSERT INTO table ... """
        columns = [str(x) for x in data.keys()]
        values = [str(x) if isinstance(x, int) else "'{}'".format(x) for x in data.values()]

        with self._db_connection:
            self._db_connection.execute(
                'INSERT INTO %s (%s) VALUES (%s);' %
                (self.table_name, ', '.join(columns), ', '.join(values)))

    def update(self, **data):
        """UPDATE table SET ..."""
        columns = [str(x) for x in data.keys()]
        values = [str(x) if isinstance(x, int) else "'{}'".format(x) for x in data.values()]
        update_data = ['{} = {}'.format(field[0], field[1]) for field in zip(columns, values)]

        with self._db_connection:
            self._db_connection.execute(
                'UPDATE %s SET %s;' %
                (self.table_name, ', '.join(update_data)))

    def delete(self):
        """DELETE FROM table """
        with self._db_connection:
            return self._db_connection.execute("DELETE FROM %s" % self.table_name)

    def delete_table(self):
        """ DROP TABLE IF EXISTS table """
        with self._db_connection:
            self._db_connection.execute("DROP TABLE IF EXISTS %s" % self.table_name)
