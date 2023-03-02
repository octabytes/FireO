from datetime import datetime

from fireo.fields import Field, errors
from google.cloud import firestore
from google.cloud.firestore_v1.transforms import Sentinel
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


class DateTime(Field):
    """Date Time field for firestore

    allowed_attributes = [auto, auto_update]

    auto: If True, then on save it will set the current datetime
    auto_update: If True, then on update it will set the current datetime

    Examples
    --------
        class User(Model):
            created = DateTime()

        u = User()
        u.created = datetime.datetime.now()
    """

    allowed_attributes = ['auto', 'auto_update']

    empty_value_attributes = allowed_attributes

    def attr_auto(self, attr_val, field_val):
        """Method for attribute auto"""
        if field_val is None and attr_val:
            return firestore.SERVER_TIMESTAMP
        return field_val

    def attr_auto_update(self, attr_val, field_val):
        """Method for attribute auto"""
        if attr_val:
            return firestore.SERVER_TIMESTAMP
        return field_val

    # Override method
    def db_value(self, val):
        if isinstance(val, (DatetimeWithNanoseconds, datetime, Sentinel, type(None))):
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {datetime}, '
                                      f'got {type(val)}')
