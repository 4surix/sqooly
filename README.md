# SQooLy

Sqooly is a ORM (i try) SQLite for Python.

# Exemple 

```python
import database


class User:

    def __init__(self, data:tuple):
        self.id, self.name = data

    def modify_name(self, name:str):
        database.users.modify_name((name, self.id))


def get(uid:int):

    data:tuple = database.users.get_with_id(uid).fetchone()

    if data:
        return User(data)
```