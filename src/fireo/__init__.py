from google.cloud import firestore

from fireo.utils.utils import GeoPoint
from fireo.database import connection, db
from fireo.transaction import Transaction

def transaction(**kwargs):
    return db.conn.transaction(**kwargs)


def batch():
    return db.conn.batch()


def transactional(to_wrap):
    return Transaction(to_wrap)


def ListUnion(values):
    return firestore.ArrayUnion(values)


def ListRemove(values):
    return firestore.ArrayRemove(values)


def Increment(value):
    return firestore.Increment(value)


def list_collections():
    """Returns a list of all collections"""
    return [c.id for c in db.conn.collections()]
