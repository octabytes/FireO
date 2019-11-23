import inspect

from fireo.database import db
from fireo.utils import utils
from fireo.queries import errors


class BaseQuery:
    """Create connection with firestore and provide ref for model collection

    Methods
    -------
    set_collection_path(path, key):
        Set collection path

    get_ref():
        Provide firestore ref for model collection

    set_group_collection():
        setter method for group collection

    validate_key():
        Validate the key
    """

    def __init__(self, model_cls):
        self.model_cls = model_cls
        # if collection path and model key both are not available then
        # collection_name will be the base collection path
        self.collection_path = model_cls.collection_name
        # Firestore allow to get documents from group collection
        self.group_collection = False

    def set_collection_path(self, path=None, key=None):
        """Set collection path"""
        # Check collection path is given if not then get it from model key
        if path:
            self.collection_path = path + '/' + self.model_cls.collection_name
        elif key:
            self.collection_path = utils.collection_path(key)

    def get_ref(self):
        """Provide firestore ref for model collection"""

        #  Validate the key
        self.validate_key()

        if self.group_collection:
            return db.conn.collection_group(self.collection_path)

        return db.conn.collection(self.collection_path)

    def set_group_collection(self, is_group):
        """Set group collection"""
        self.group_collection = is_group

    def validate_key(self):
        """Validate key, Key collection must be the same as the model collection name

        Examples
        --------
        .. code-block:: python
            class User(Model):
                name = TextField()

            u = User.collection.create(name="Azeem")

            Student.collection.get(u.key)  # Invalid key because collection is student and key is for User

            # Valid key
            User.collection.get(u.key)

        Raises
        ------
        InvalidKey:
            If collection path in key is not same as the model collection name
        """
        # Get model name because when document is saving model instance is passed instead of
        # model class for modifying the model instance
        if inspect.isclass(self.model_cls):
            model_name = self.model_cls.__name__
        else:
            model_name = self.model_cls.__class__.__name__
        # Check collection is not parent
        if '/' not in self.collection_path:
            # check collection path is the same as collection name
            if self.collection_path != self.model_cls.collection_name:
                raise errors.InvalidKey(f'Invalid key is given, expected "{model_name}" type key, '
                                        f'got "{self.collection_path}" type key')
        else:
            # If collection path is contains the parent then
            # Get last name from collection path
            # For example if collection path is "user/doc_id/student/student_doc_id then student
            # will be the collection name
            key_collection = self.collection_path.split('/')[-1]
            if key_collection != self.model_cls.collection_name:
                raise errors.InvalidKey(f'Invalid key is given, expected "{model_name}" type key, '
                                        f'got "{key_collection}" type key')
