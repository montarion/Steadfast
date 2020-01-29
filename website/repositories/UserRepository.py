from flata import Flata, Query
from flata.storages import JSONStorage

from model.User import User


class UserRepository(object):
    def __init__(self):
        self.db = self.setup("users")
        self.q = Query()

    @staticmethod
    def setup(table_name: str):
        """Creates the specified table if not yet exists in the db.json and returns its reference either way"""
        db = Flata('db.json', storage=JSONStorage)
        db.table(table_name, id_field="id")
        return db.get(table_name)

    def user_exists(self, user: User):
        if self.get_by_id(user.email):
            return True
        return False

    def add(self, user: User):
        if not self.user_exists(user):
            self.db.insert(user.__dict__)
            addedUser = self.get_by_id(user.email)
            return User(addedUser['email'], addedUser['username'])
        else:
            raise Exception("User with email: " + user.email + " already exists")

    def get_by_id(self, email: str):
        """returns empty list if nothing is found"""
        return self.db.search(self.q.email == email)[0]
