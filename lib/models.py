# from abc import ABC


class Base():

    __tablename__ = None

    def __init__(self, connection):
        self._connection = connection
        self.schema = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('_')}
        self.columns = [k for k, v in self.schema.items()]

    def create_table(self):
        """ Create table from definition in class model """
        schema = ["%s %s" % (k, v[0].__name__) for k, v in self.schema.items()]
        with self._connection:
            self._connection.execute(
                'CREATE TABLE %s (%s);' % (self.__class__.__tablename__, ', '.join(schema)))

    def select_all(self):
        return self._connection.execute(
            'SELECT %s FROM %s;' % (', '.join(self.columns), self.__class__.__tablename__))

    def insert(self, **data):
        if not data:
            raise ValueError
        self._validate_schema(data)

        columns = [str(x) for x in data.keys()]
        values = [str(x) if isinstance(x, int) else "'{}'".format(x) for x in data.values()]
        with self._connection:
            self._connection.execute(
                'INSERT INTO %s (%s) VALUES (%s);' %
                (self.__class__.__tablename__,
                 ', '.join(columns),
                 ', '.join(values)))

    def update(self, **data):
        if not data:
            raise ValueError
        self._validate_schema(data)

        columns = [str(x) for x in data.keys()]
        values = [str(x) if isinstance(x, int) else "'{}'".format(x) for x in data.values()]
        update_data = ['{} = {}'.format(field[0], field[1]) for field in zip(columns, values)]

        with self._connection:
            self._connection.execute(
                'UPDATE %s SET %s;' %
                (self.__class__.__tablename__,
                 ', '.join(update_data)))

    def delete(self):
        with self._connection:
            return self._connection.execute("DELETE FROM %s" % self.__class__.__tablename__)

    def delete_table(self):
        with self._connection:
            self._connection.execute("DROP TABLE IF EXISTS %s" % self.__class__.__tablename__)

    def _validate_schema(self, data):
        for key, value in data.items():
            if key not in self.columns or not isinstance(value, self.schema[key][0]):
                raise ValueError


class User(Base):

    __tablename__ = 'users'

    id = (int, 'required')
    username = (str, 'not_required')
