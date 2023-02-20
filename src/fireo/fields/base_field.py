from fireo.fields.field_attribute import FieldAttribute
from fireo.utils.types import DumpOptions, LoadOptions


class MetaField(type):
    """Get allowed attributes for Fields"""

    def __new__(mcs, name, base, attrs):
        cls = super().__new__(mcs, name, base, attrs)

        allow_attr = cls.allowed_attributes
        for b in base:
            allow_attr += b.allowed_attributes

        setattr(cls, "allowed_attributes", allow_attr)
        return cls


class Field(metaclass=MetaField):
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

    name:
        name of the field

    model_cls:
        Class of the model

    field_attribute:
        Parse field attributes

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

    empty_value_attributes = []

    def __init__(self, *args, **kwargs):
        self.raw_attributes = kwargs
        self.name = None
        self.model_cls = None
        self.field_attribute = FieldAttribute(self, kwargs)

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
        self.model_cls = model_cls
        setattr(model_cls, name, None)
        model_cls._meta.add_field(self)

    @property
    def db_column_name(self):
        """Get field according to column name

        Return the name of the field according to `column_name` attribute if no `column_name` is
        specify then same field name will return
        """
        return self.raw_attributes.get("column_name") or self.name

    def get_value(self, val, dump_options=DumpOptions()):
        """Get field value after validation

        Make validation and applying attribute function on it.
        it will return the `db_value` how this is going to save in firestore

        Parameters
        ----------
        val : Any
            Field value

        dump_options : DumpOptions
            Options for dumping to Firestore dictionary

        Returns
        -------
            DB value
        """
        val = self.field_attribute.parse(
            val,
            dump_options.ignore_required,
            dump_options.ignore_default,
        )
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
        if self.model_cls:
            # check if user defined to set the value as lower case
            if self.model_cls._meta.to_lowercase:
                return val.lower() if type(val) is str else val
        return val

    def field_value(self, val, load_options=LoadOptions()):
        """ How this field represent value that is coming from firestore

        Value can be modified after getting value from firestore

        Example
        -------
            .. code-block:: python
                class BoolField(Field):
                    def field_value(self, val, model):
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
            model:
                Model instance
            initial:
                Is it initial value or not
        """
        return val
