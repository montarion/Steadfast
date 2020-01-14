from flata import Flata, Query, where
from flata.storages import JSONStorage
import json


class Repository(object):
    def __init__(self, table_name: str, id_field: str = "id"):
        self.db = self.setup(table_name, id_field)
        self.q = Query()

    @staticmethod
    def setup(table_name: str, id_field: str):
        """Creates the specified table if not yet exists in the db.json and returns its reference either way"""
        db = Flata('repositories/db.json', storage=JSONStorage)
        db.table(table_name, id_field=id_field)
        return db.get(table_name)

    def get_all(self):
        return self.db.all()

    def get_all_operation_names(self):
        return list(set([image['operation_name'] for image in self.db.all()]))

    def get_by_id(self, identity: int):
        """returns empty list if nothing is found"""
        return self.db.search(self.q.id == identity)

    def get_by_operation(self, operation_name: str):
        """e.g. http://0.0.0.0:5000/api/operations/pokemon"""
        return self.db.search(self.q.operation_name == operation_name)

    def insert(self, obj: dict):
        """if image_name does not yet exist, insert"""
        if not self.db.search(self.q.image_name == obj['image_name']):
            self.db.insert(obj)
        else:
            raise Exception('this image_name already exists')

    def update(self, obj: dict):
        """Update an object, the object *must* contain it's image_name for identity"""
        self.db.update(obj, where('image_name') == obj['image_name'])

    def remove(self, identity: int):
        try:
            self.db.remove(ids=[identity])
        except KeyError:  # entry doesn't exist
            #print(f'The id: {str(identity)} could not be found while trying to remove') # that's not how you do formatting
            print("The id: {} could not be found while trying to remove.".format(str(identity)))

    def remove_by_property(self, prop: str, val):
        """warn: this doesn't throw an error when nothing is found"""
        self.db.remove(self.q[prop] == val)
        print(f'removed entry with prop: {prop} and val: {str(val)}')
