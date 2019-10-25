from fireo.fields import Field, errors


class BooleanField(Field):
    """Boolean field for firestore

    Examples
    -------
        class User(Model):
            is_student = BooleanField()

        u = User()
        u.is_student = True
    """

    # Override method
    def db_value(self, val):
        if type(val) is bool or val is None:
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {bool}, '
                                      f'got {type(val)}')
