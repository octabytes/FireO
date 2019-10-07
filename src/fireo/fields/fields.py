from fireo.fields.field_validation import FieldValidation


class Field:
    """Base Field contain common method for all fields

    All fields should be sub class of this `Field` class. Different type of fields handle
    different type of data.

    Attributes
    ----------
    allowed_attributes : list
        Allowed attribute for each fields. This allow to add extra functionality for fields

        Examples
        ---------
        .. code-block:: python
            class User(Model):
                name = TextField(column_name="full_name")

        In firestore this fields will be store as **full_name**

    db_column_name : str
        return the name of the field according to `column_name` attribute if no `column_name` is
        specify then same field name will return

    Methods
    -------
    contribute_to_model(mdoel_cls, name):
        Attach the field to model `_meta`

    get_value(val):
        Make validation and return the field db value

    db_value(val):
        How this field is going to save in firestore, Value can be modified here before saving

    field_value(val):
        How this field represent value that is coming from firestore
    """
    allowed_attributes = []

    def __init__(self, *args, **kwargs):
        self.raw_attributes = kwargs
        self.name = None
        self.validation = FieldValidation(self, kwargs)

    def contribute_to_model(self, model_cls, name):
        """Attach field to model class

        This method attach field to model class in `_meta` and make this field to `None`

        Parameters
        ----------
        model_cls : Model
            In which model this field will be attached

        name : str
            What is the name of this field when it is attaching with model
        """
        self.name = name
        setattr(model_cls, name, None)
        model_cls._meta.add_field(self)

    @property
    def db_column_name(self):
        """Get field according to column name

        Return the name of the field according to `column_name` attribute if no `column_name` is
        specify then same field name will return
        """
        return self.raw_attributes.get("column_name") or self.name

    def get_value(self, val):
        """Get field value after validation

        Make validation and applying attribute function on it.
        it will return the `db_value` how this is going to save in firestore

        Parameters
        ----------
        val : Any
            Field value

        Returns
        -------
            DB value
        """
        v = self.validation.validate(val)
        return self.db_value(val)

    def db_value(self, val):
        """How the value is going to save in firestore

        How this field is going to save in firestore, Value can be modified here before saving
        in firestore.

        Example
        -------
            .. code-block:: python
                class BoolField(Field):
                    def db_value(self, val):
                        if val == True:
                            return 1
                        else:
                            return 0

                class User(Model):
                    is_student = BoolField()

                u = User()
                u.is_student = True

            This will save **1** in firestore

        Returns
        ------
            val:
                Modified value
        """
        return val

    def field_value(self, val):
        """ How this field represent value that is coming from firestore

        Value can be modified after getting value from firestore

        Example
        -------
            .. code-block:: python
                class BoolField(Field):
                    def field_value(self, val):
                        if val == 1:
                            return True
                        else:
                            return False

                class User(Model):
                    is_student = BoolField()

                u = User.collection.get(id="xHuJujlUBkn")
                if u.is_student == True:
                    print("This user is student")

        Returns
        ------
            val:
                Modified value
        """
        return val


class IDField(Field):
    """Specify custom id for models

    User can specify model id and will save with the same id in firestore otherwise it will
    return None and generate later from firestore and attached to model

    Example
    --------
    .. code-block:: python
        class User(Mode):
            user_id = IDField()

        u = User()
        u.user_id = "custom_doc_id"
        u.save()

        # After save id will be saved in `user_id`
        print(self.user_id)  # custom_doc_id
    """
    def contribute_to_model(self, model_cls, name):
        self.name = name
        setattr(model_cls, name, None)
        model_cls._meta.add_model_id(self)


class NumberField(Field):
    """Number field for Models

    Define numbers for models integer, float etc

    Examples
    --------
        class User(Model):
            age = NumberField()
    """
    pass


class TextField(Field):
    """Text field for Models

        Define text for models

        Examples
        --------
            class User(Model):
                age = TextField()
        """
    pass