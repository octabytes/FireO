from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove

from fireo.fields import Field, errors


class ListField(Field):
    """Array field for firestore

    Example
    -------
        class User(Model):
            subjects = ListField()

        u = User()
        u.subjects = ['English', 'Math']
    """

    # Override method
    def db_value(self, val):
        if type(val) in [list, ArrayUnion, ArrayRemove] or val is None:
            # check if user defined to set the value as lower case
            if self.model_cls._meta.to_lowercase:
                return [v.lower() if type(v) is str else v for v in val]
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {list}, '
                                      f'got {type(val)}')
