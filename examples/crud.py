from lib.core import Database
from examples.models import User


if __name__ == '__main__':
    conn = Database(db_name='test_db.sqlite').get_connection()

    # Create a table with name defined in __tablename__ attr of the model class.
    User(conn).create_table()

    # Insert a new row in the table. Currently ORM doesn't support uniqueness for pk.
    User(conn).insert(id=21, username='Ivan')

    # Uncomment line below to update ALL the rows in the table with the values.
    # User(conn).update(id=1, username='John')

    # Search for all rows in table, then iterate over it
    print([x for x in User(conn).select_all()])

    # Uncomment line below to delete ALL rows in the related table
    # User(conn).delete()

    # Uncomment line below to DROP the table. This will delete data and schema.
    # User(conn).delete_table()
