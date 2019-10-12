from fireo.database.errors import DBConnectionError
from google.cloud import firestore


class Database:
    """Create connection with google cloud firestore

    Responsible to create and verify connection is successfully establish.

    If you’re running in Compute Engine or App Engine, authentication should “just work”.
    If you’re developing locally, the easiest way to authenticate is using the Google Cloud SDK:

    If you’re running your application elsewhere, you should download a service account JSON keyfile
    and point to it using an environment variable

    More about Authentication: https://googleapis.dev/python/google-api-core/latest/auth.html

    Attributes
    ----------
    conn : firestore.Client()
        return the connection from firestore

    Methods
    -------
    connect():
        create a connection with firestore

    Raises
    ------
    DBConnectionError:
        Missing or wrong project id and credentials
    """

    def __init__(self):
        self._conn = None

    def connect(self):
        #self._conn = "asdsad"
        self._conn = firestore.Client()

    @property
    def conn(self):
        if self._conn is None:
            raise DBConnectionError("Unable to connect with Firestore")
        return self._conn

