# py_fatless_orm
Ridiculously simple ORM (Object-Relational Mapping) layer to get your Python objects talking with SQLite

# Key features
* Complete Object-specified communication with the DB. Save time on constructing SQL queries, use your Python objects instead!
* Supports create/delete tables, insert/update/remove values (rows)
* DB consistency with built in automated functions:
**  DB connection open and close on each request despite it result (failed/success).
**  Commit on each success request and transaction rollback on failed requests.
**  DB schema validation on INSERT/UPDATE requests.

# Not available, but planned to implement:
* Filters/Order By/Group By
* Primary Key (PK) / Foreign Key (FK)
* 'required'/'not_required' flag processing on schema


# Installation
Once you've cloned the repo from GitHub, make sure you've created a virtual environment for experiments.
```
sudo pip3 install virtualenv
python3 -m virtualenv ./venv
source venv/bin/activate
```

# Usage
Basic CRUD (Create-Read-Update-Delete) operations using the ORM are demonstrated in examples/examples.py, so you could open it in your IDE (like PyCharm) and simply run the script.

Alternatively, you could use the ORM as a library.

DB model classes currently resides in lib/models.py, on your own project it may resides on your choice, but bear in mind mandatory conditions that should be met in order to your class considered as DB model:
1. It must be derived from 'Base' class (from lib/models.py)
2. It must have __tablename__ attribute with string value (ascii symbols, preferably)
3. It must contain number of desired fields (columns) defined to be created/used for that table.
Use following format and arguments order. Please, see the [SQLite and Python types](https://docs.python.org/3/library/sqlite3.html#sqlite-and-python-types) for list of supported types.

name = (type, 'required'/'not_required')

```
# content of lib/models.py

class User(Base):

    __tablename__ = 'users'

    id = (int, 'required')
    username = (str, 'not_required')
```

Back to usage. First we need to import the 'Database' class from core and DB models classes, like 'User' in the example:
```
# content of examples/models.py

from lib.core import Database
from lib.models import User
```

We would need to create a connection object from Database (yet you may set your own 'provider' instead of sqlite3 or 'db_name')
```
# content of examples/models.py

conn = Database(db_name='test_db.sqlite').get_connection()
```

Now you can rock and roll with your DB without writing a piece of SQL!
```
# content of examples/models.py

# Create a table with name defined in __tablename__ attr of the model class.
User(conn).create_table()

# Insert a new row in the table. Currently ORM doesn't support uniqueness or pk.
User(conn).insert(id=21, username='Ivan')

# Update ALL the rows in the table with the values.
User(conn).update(id=1, username='John')

# Search and print all rows in table. Method select_all() returns an iterable sqlite3.Cursor object.
print([x for x in User(conn).select_all()])

# Remove ALL rows in the related table. Keep the schema.
User(conn).delete()

# DROP the table. This will delete data and schema.
User(conn).delete_table()
```