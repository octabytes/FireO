from fireo.fields import Field, errors
from google.cloud import firestore


class GeoPoint(Field):
    """GeoPoint field for firestore

    Examples
    -------
    .. code-block:: python
        class User(Model):
            location = GeoPoint()

        u = User()
        u.location = fireo.GeoPoint(latitude=123.23, longitude=421.12)
    """

    # Override method
    def db_value(self, val):
        if type(val) is firestore.GeoPoint or val is None:
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {firestore.GeoPoint}, '
                                      f'got {type(val)}')