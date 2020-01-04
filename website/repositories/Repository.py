from flata import Flata, Query, where
from flata.storages import JSONStorage
import json


class Repository(object):
    def __init__(self, table_name):
        self.db = self.setup(table_name)
        self.q = Query()

    @staticmethod
    def setup(table_name):
        """Creates the specified table if not yet exists in the db.json and returns its reference either way"""
        db = Flata('repositories/db.json', storage=JSONStorage)
        db.table(table_name, id_field="id")
        return db.get(table_name)

    def get_all(self):
        return self.db.all()

    def get_by_id(self, identity: int):
        """returns empty list if nothing is found"""
        return self.db.search(self.q.id == identity)

    def get_by_operation(self, operation_name: str):
        return self.db.search(self.q.operation_name == operation_name)

    def insert(self, obj):
        """if image_name does not yet exist, insert"""
        if not self.db.search(self.q.image_name == obj['image_name']):
            self.db.insert(obj)
        else:
            raise Exception('this image_name already exists')

    def update(self, obj):
        """Update an object, the object should contain it's image_name for identity"""
        self.db.update(obj, where('image_name') == obj['image_name'])

    def remove(self, identity):
        try:
            self.db.remove(ids=[identity])
        except KeyError:  # entry doesn't exist
            print(f'The id: {str(identity)} could not be found while trying to remove')
            pass

    def remove_by_property(self, prop: str, val):
        """warn: this doesn't throw an error when nothing is found"""
        self.db.remove(self.q[prop] == val)
        print(f'removed entry with prop: {prop} and val: {str(val)}')
