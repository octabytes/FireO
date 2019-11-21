from fireo.fields import Field, errors


class MapField(Field):
    """Map field for firestore

    Examples
    --------
    .. code-block:: python
        class User(Model):
            marks = MapField()

        u = User()
        u.marks = {'Math': 70, 'English': 80}
    """

    # Override method
    def db_value(self, val):
        if type(val) is dict or val is None:
            # check if user defined to set the value as lower case
            if self.model_cls._meta.to_lowercase:
                return {k: v.lower() if type(v) is str else v for k,v in val.items()}
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {dict}, '
                                      f'got {type(val)}')
