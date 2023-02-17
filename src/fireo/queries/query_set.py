from fireo.queries.delete_query import DeleteQuery
from fireo.queries.filter_query import FilterQuery
from fireo.queries.get_query import GetQuery
from fireo.queries.create_query import CreateQuery
from fireo.queries.refresh_query import RefreshQuery
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

    def create(self, mutable_instance=None, transaction=None, batch=None, merge=None, no_return=False, **kwargs):
        """Create new document in firestore collection

        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        no_return: bool
            If set True then return nothing otherwise return model object

        transaction:
            Firestore transaction

        batch:
            Firestore batch writes

        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            modified instance or new instance if no mutable instance provided
        """
        transaction_or_batch = transaction if transaction is not None else batch
        return CreateQuery(self.model_cls, mutable_instance, no_return, **kwargs).exec(transaction_or_batch, merge)

    def update(self, mutable_instance, transaction=None, batch=None):
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

        batch:
            Firestore batch writes

        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            updated modified instance
        """
        transaction_or_batch = transaction if transaction is not None else batch
        return UpdateQuery(self.model_cls, mutable_instance).exec(transaction_or_batch)

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

    def refresh(self, mutable_instance, transaction=None):
        """Refresh document from firestore

        Parameters
        ----------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        transaction:
            Firestore transaction

        Returns
        -------
        Model instance:
            wrap query result into model instance
        """
        return RefreshQuery(self.model_cls, mutable_instance).exec(transaction)

    def filter(self, parent=None, *args, **kwargs):
        """Filter document from firestore

        Parameters
        ----------
        parent:
            Parent collection if any
        args:
            Where clauses document filter on the base of this

        kwargs:
            keyword args Direct assign for equal filter
        """
        return FilterQuery(self.model_cls, parent, *args, **kwargs)

    def delete(self, key, transaction=None, batch=None, child=False):
        """Delete document from firestore

        Parameters
        ----------
        key : str
            key of the document

        transaction:
            Firestore transaction

        batch:
            Firestore batch writes
        """
        transaction_or_batch = transaction if transaction is not None else batch
        DeleteQuery(self.model_cls, key, child=child).exec(
            transaction_or_batch)
