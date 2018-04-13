from .core import Query


class Base:

    __tablename__ = None

    def __init__(self, connection):
        self._connection = connection
        self.schema = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('_')}
        self.columns = [k for k, v in self.schema.items()]

    def create_table(self):
        """ Create table from definition in class model """
        schema = ["%s %s" % (k, v[0].__name__) for k, v in self.schema.items()]
        return Query(self._connection, self.__class__.__tablename__).create_table(schema)

    def select_all(self):
        """ Select all rows for columns defined in class model """
        return Query(self._connection, self.__class__.__tablename__).fetchall(self.columns)

    def insert(self, **data):
        """ Insert a new row with arbitrary number of key=value pairs (should match to table schema) """
        if not data:
            raise ValueError
        self._validate_schema(data)
        return Query(self._connection, self.__class__.__tablename__).insert(**data)

    def update(self, **data):
        """ Update existing row(s) with arbitrary number of key=value pairs (should match to table schema) """
        if not data:
            raise ValueError
        self._validate_schema(data)
        return Query(self._connection, self.__class__.__tablename__).update(**data)

    def delete(self):
        return Query(self._connection, self.__class__.__tablename__).delete()

    def delete_table(self):
        return Query(self._connection, self.__class__.__tablename__).delete_table()

    def _validate_schema(self, data):
        for key, value in data.items():
            if key not in self.columns or not isinstance(value, self.schema[key][0]):
                raise ValueError
