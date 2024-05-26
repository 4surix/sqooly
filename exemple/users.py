# encode: utf-8
# Python 3.10.12
# ----------------------------------------------------------------------------

import database


class User:

    def __init__(self, data):

        (
            self.id,
            self.name
        ) = data

    def modify_name(self, name:str):
        database.users.modify_name((name, self.id))


def get(uid:int):

    data = database.users.get(uid).fetchone()

    if data:
        return User(data)
