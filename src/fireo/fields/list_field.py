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
        if type(val) is list or val is None:
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {list}, '
                                      f'got {type(val)}')
