from fireo.database import db
from fireo.fields.base_field import Field
from fireo.fields import errors
from fireo.utils import utils
from google.cloud import firestore









class TextField(Field):
    """Text field for Models

        Define text for models

        Examples
        --------
            class User(Model):
                age = TextField()
        """
    pass

