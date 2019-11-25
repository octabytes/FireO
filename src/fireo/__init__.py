from fireo.utils.utils import GeoPoint
from fireo.database import connection, db
from fireo.transaction import Transaction


def transaction(**kwargs):
    return db.conn.transaction(**kwargs)


def batch():
    return db.conn.batch()


def transactional(to_wrap):
    return Transaction(to_wrap)