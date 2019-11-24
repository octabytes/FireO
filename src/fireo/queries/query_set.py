from fireo.queries.delete_query import DeleteQuery
from fireo.queries.filter_query import FilterQuery
from fireo.queries.get_query import GetQuery
from fireo.queries.create_query import CreateQuery
from fireo.queries.update_query import UpdateQuery


class QuerySet:
    """Provide operations related to firestore

    Methods
    -------
    create(kwargs):
        Create new document in firestore collection

    update(kwargs):
        Update existing document in firestore collection

    get(key)
        Get document from firestore

    delete(key)
        Delete document in firestore
    """
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def create(self, mutable_instance=None, transaction=None, **kwargs):
        """Create new document in firestore collection

        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        transaction:
            Firestore transaction

        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            modified instance or new instance if no mutable instance provided
        """
        return CreateQuery(self.model_cls, mutable_instance, **kwargs).exec(transaction)

    def update(self, mutable_instance=None, transaction=None, **kwargs):
        """Update existing document in firestore collection

        Parameters
        ---------
        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        transaction:
            Firesotre transaction

        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            updated modified instance
        """
        return UpdateQuery(self.model_cls, mutable_instance, **kwargs).exec(transaction)

    def get(self, key, transaction=None):
        """Get document from firestore

        Parameters
        ----------
        key : str
            key of the document

        transaction:
            Firestore transaction

        Returns
        -------
        Model instance:
            wrap query result into model instance
        """
        return GetQuery(self.model_cls, key).exec(transaction)

    def filter(self, parent=None, *args):
        """Filter document from firestore

        Parameters
        ----------
        parent:
            Parent collection if any
        args:
            Where clauses document filter on the base of this
        """
        return FilterQuery(self.model_cls, parent, *args)

    def delete(self, key, transaction=None):
        """Delete document from firestore

        Parameters
        ----------
        key : str
            key of the document

        transaction:
            Firestore transaction
        """
        DeleteQuery(self.model_cls, key).exec(transaction)