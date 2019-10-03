from fireo.database.errors import DBConnectionERR
from google.cloud import firestore


class Database:

    def __init__(self):
        self._conn = "todo"
        #self._conn = firestore.Client()

    @property
    def conn(self):
        if self._conn is None:
            raise DBConnectionERR("Unable to connect with Firestore")
        return self._conn


db = Database()
