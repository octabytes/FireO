from fireo.database import db


class BaseQuery:
    """Create connection with firestore and provide ref for model collection

    Methods
    -------
    get_ref():
        Provide firestore ref for model collection
    """
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def get_ref(self):
        """Provide firestore ref for model collection"""
        ref = db.conn.collection(self.model_cls.collection_name)
        return ref
