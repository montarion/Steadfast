from flata import Flata, Query
from flata.storages import JSONStorage

from model.User import User


class UserRepository(object):
    def __init__(self):
        self.db = self.setup("users", "email")
        self.q = Query()

    @staticmethod
    def setup(table_name: str, id_field: str):
        """Creates the specified table if not yet exists in the db.json and returns its reference either way"""
        db = Flata('repositories/db.json', storage=JSONStorage)
        db.table(table_name, id_field=id_field)
        return db.get(table_name)

    def insert(self, user: User):
        self.db.insert(user.__dict__)

    def get_by_id(self, email: str):
        """returns empty list if nothing is found"""
        return self.db.search(self.q.email == email)
