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

    get(id)
        Get document from firestore

    delete(id)
        Delete document in firestore
    """
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        """Create new document in firestore collection

        Parameters
        ---------
        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            modified instance or new instance if no mutable instance provided
        """
        return CreateQuery(self.model, **kwargs).exec()

    def update(self, **kwargs):
        """Update existing document in firestore collection

        Parameters
        ---------
        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            updated modified instance
        """
        return UpdateQuery(self.model, **kwargs).exec()

    def get(self, id):
        """Get document from firestore

        Parameters
        ----------
        id : str
            Id of the document

        Returns
        -------
        Model instance:
            wrap query result into model instance
        """
        return GetQuery(self.model, id).exec()

    def filter(self, *args):
        """Filter document"""
        return FilterQuery(self.model, *args)

    def delete(self, id):
        """Delete document from firestore

        Parameters
        ----------
        id : str
            Id of the document

        Returns
        -------
        id : str, None
            return document id or None
        """
        return DeleteQuery(self.model, id).exec()