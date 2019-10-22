from fireo.database.errors import DBConnectionError
from google.cloud import firestore
import grpc
from google.cloud.firestore_v1.gapic import firestore_client
from google.cloud.firestore_v1.gapic.transports import firestore_grpc_transport


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

    local_connection():
        Local firestore connection for testing

    Raises
    ------
    DBConnectionError:
        Missing or wrong project id or credentials
    """

    def __init__(self):
        self._conn = None

    def connect(self,credentials=None, from_file=None):
        try:
            if credentials:
                self._conn = firestore.Client(credentials=credentials)
            elif from_file:
                self._conn = firestore.Client.from_service_account_json(from_file)
            else:
                raise DBConnectionError("Credentials or service account json file required to connect with firestore")
        except Exception as e:
            raise DBConnectionError(e) from e

    def local_connection(self):
        self._conn = firestore.Client()
        channel = grpc.insecure_channel("localhost:8080")
        transport = firestore_grpc_transport.FirestoreGrpcTransport(channel=channel)
        self._conn._firestore_api_internal = firestore_client.FirestoreClient(transport=transport)

    @property
    def conn(self):
        if self._conn is None:
            self._conn = firestore.Client()
        return self._conn

