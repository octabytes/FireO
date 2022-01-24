from fireo.fields.errors import FieldNotFound, MissingFieldOptionError
from fireo.managers import managers
from fireo import fields
from fireo.models.errors import NonAbstractModel, UnSupportedMeta
from fireo.utils import utils


class ModelMeta(type):
    """Create fields, manager and other stuff for Models

    Add `_meta` attribute to each Model which hold all the information about fields, managers and any
    other stuff related to model. Also responsible to generate collection name from model.

    Methods
    -------
    __new__(mcs, name, base, attrs):
        Create modified type for model class
    """

    def __new__(mcs, name, base, attrs):
        """Create modified type for model class

        Convert fields, managers and other stuff into `Meta` class and attached it with model class

        Attributes
        ----------
        _meta : Meta()
            Hold all information about you model, can be accessible via class **cls._meta**

        collection_name : str
            Name of collection which is saved in database if user not provided any collection name
            then `Meta` class generate it from Model name and attach it with class can be accessible
            via class **cls.collection_name**

        Returns
        -------
            Modified type for model class
        """
        cls = super().__new__(mcs, name, base, attrs)

        # check user specify any additional meta data for this model or not
        # For example collection name etc if there is not then assign None to it
        if 'Meta' not in attrs:
            cls.Meta = None

        class Meta:
            """Hold information about fields, manager and other model related stuff

            Meta class get fields, manager and other model related stuff and attach it to
            with model class.

            For example:
                class User:
                    name = TextField()
                    age = NumberField()

                u = User()
                u.name = "Azeem"
                u.age = 25

                This Meta class is responsible to attach these fields with model class
                later on these fields can be accessible via **cls._meta**

                For example:
                    cls._meta.field_list() will return {name: <obj of TextField ox13>, age: <obj of NumberField 0x17>}

                Later on you can use these fields to get corresponding value from model and use them further
                field value can be get like this:

                    getattr(self, field_name)

                Here `self` is instance of model class and `field_name` is one the name from `field_list()`

                In above example if you run this

                    getattr(model_instance, name)
                    getattr(model_instance, age)

                it will return **Azeem** and **25**

            Attributes
            ----------
            field_list : dict
                Contain all model field

            id : str, optional
                Model id if not specify then it return `None` and later create by firestore
                and attach to model

            abstract: bool
                Model is abstract or not

            missing_field: str
                Model config what to do with fields that are comming from firestore and not in model
                possible values are (merge, ignore, raise_error) merge is default

            to_lowercase: bool
                Firestore is case sensitive convert all value in lowercase if set True. By default
                it set False.

            collection : manager
                Collection is class level attribute can be used to access the manager

            See Also
            --------
            fireo.managers.Manager :
                Manager are responsible to run certain functions on firestore like creating collection
                getting documents update etc

            Methods
            -------
            add_model_id(field):
                If user specify any id then attach this id to model

            add_field(field):
                All all user specified fields in Model class

            get_field(name):
                Get field from model on the base of name

            get_field_by_column_name(name):
                Get field according to firestore column name(field name)

            set_user_defined_meta(user_meta):
                Set user defined meta in model class, These meta is actually the config for model

            Raises:
            -------
            FieldNotFound:
                if there is no such in field in model class

            NonAbstractModel:
                If any model is inherit from non abstract model
            """
            field_list = {}  # Hold all the model fields
            id = None  # Model id if user specify otherwise just None will generate late by firestore automatically

            def __init__(self):
                # Convert Model class into collection name
                # change it to lower case and snake case
                # e.g UserCollection into user_collection
                self.collection_name = utils.collection_name(cls.__name__)
                self.abstract = False
                self.missing_field = 'merge'
                self.ignore_none_field = True
                self.to_lowercase = False
                self._referenceDoc = None

            # Attached manager to model class
            # later on manager can be accessible via class `collection` attribute
            # like this **cls.collection**
            if 'collection' not in cls.__dict__:
                manager = managers.Manager()
                manager.contribute_to_model(cls)

            def add_model_id(self, field):
                """ Attach user define id to model

                If user specify any custom id for this model
                attach it to model this contains two thing custom id and if field

                For Example:
                    class User:
                        user_id = IDField()

                    In this case it will hold (user_id, <obj of IDField 0x137>)

                    later `id` can be accessible via `_meta`
                    like this **cls._meta.id**

                Parameters
                ----------
                field : IDField()
                    User defined custom id field
                """
                self.id = (field.name, field)

            def add_field(self, field):
                """Add model fields into model meta class

                These fields can be used later for getting corresponding values from
                model instance and some other operations

                can be accessible via `_meta`
                like this **cls._meta.field_list()**

                Parameters
                ----------
                field : Field
                    This can be any type which is derived from `Field` sub class
                    For example `TextField`, `NumberField` etc
                """
                self.field_list[field.name] = field

            def get_field(self, name):
                """Get model field from field list

                Get field on the base of it's name can be accessible via `_meta`
                like this **cls._meta.get_field(name)**

                Parameters
                ---------
                name:
                    Field name

                Returns
                ------
                    Model field

                Raises
                ------
                FieldNotFound:
                    If field not found in model
                """
                if name in self.field_list:
                    return self.field_list[name]
                raise FieldNotFound(f'Field "{name}" not found in model "{cls.__name__}"')

            def get_field_by_column_name(self, name):
                """Get field by column name

                User can also define different name for each field to save in firestore
                Check if user specify any different name then get field corresponding to
                this db_column_name. If no column name is specify for field then just
                return the same field name

                Parameters
                ----------
                name : str
                    column name (field name) coming form firestore

                Raises
                -------
                FieldNotFound:
                    if field not found in model class and model config for `missing_field` is **raise_error**
                """
                for field in self.field_list.values():
                    if name in [field.name, field.db_column_name]:
                        return field
                if self.missing_field == 'merge':
                    f = fields.Field()
                    f.name = name
                    return f
                if self.missing_field == 'ignore':
                    return None
                if self.missing_field == 'raise_error':
                    raise FieldNotFound(f'Field "{name}" not found in model "{cls.__name__}"')

            def set_reference_doc(self, referenceDoc):
                """save the firestore reference doc for further processing"""
                self._referenceDoc = referenceDoc

            def set_user_defined_meta(self, user_meta):
                """Set user defined meta attributes for model

                User can define config by using `Meta` class in models

                Examples
                --------
                .. code-block:: python
                    class User(Model):
                        name = TextField()

                        class Meta:
                            collection_name = "user_test_collection"

                    # All the documents now save in *user_test_collection* for this model

                Parameters
                ---------
                user_meta:
                    User defined meta for model class

                Raises
                -------
                MissingFieldOptionError:
                    If option for missing_field is other than ignore, merge or raise_error
                """
                for name, val in user_meta.__dict__.items():
                    supported_meta = ['collection_name', 'abstract', 'to_lowercase', 'missing_field', 'ignore_none_field']

                    # check if name is supported by meta and name is not
                    # any special name for example '__main__, __doc__'
                    if name not in supported_meta and '__' not in name:
                        raise UnSupportedMeta(f'Meta "{name}" is not recognize in model "{cls.__name__}" '
                                              f'Possible value are {", ".join(supported_meta)}')

                    if name == 'collection_name':
                        self.collection_name = val
                    if name == 'abstract':
                        self.abstract = val
                    if name == 'to_lowercase':
                        self.to_lowercase = val
                    if name == 'ignore_none_field':
                        self.ignore_none_field = val
                    if name == 'missing_field':
                        if val in ['merge', 'ignore', 'raise_error']:
                            self.missing_field = val
                        else:
                            raise MissingFieldOptionError(
                                f'Option "{val}" is not supported by missing_field. '
                                f'Possible values are ignore, merge, raise_error')

        # Create instance of Meta class and set it to
        # Model class as _meta attribute
        _meta = Meta()
        setattr(cls, '_meta', _meta)

        # Get all fields from model and save them into `_meta.field_list()`
        # and then attach this `_meta` to model class
        for name, field in cls.__dict__.items():
            if isinstance(field, type) and name == 'Meta':
                _meta.set_user_defined_meta(field)
            if isinstance(field, (managers.Manager, fields.Field)):
                field.contribute_to_model(cls, name)

        # Get base Model if they are abstract then add these models field
        # in child classes
        #
        # For example:
        #   class AbstractModel(Model):
        #       name = TextField()
        #
        #       class Meta:
        #           abstract = True
        #
        #   class User(AbstractModel):
        #       age = NumberFiled()
        #
        #   class Student(AbstractModel):
        #       age = NumberFiled()
        #
        # Both Model user and student now contains the name field
        #
        for b in base:
            if not hasattr(b, '_meta'):
                continue
            if not b._meta.abstract:
                from fireo.models import Model
                if b != Model:
                    raise NonAbstractModel(f'Model "{cls.__name__}" can not inherit from non abstract '
                                           f'model "{b.__name__}"')
                continue
            for name, field in b._meta.field_list.items():
                # Ignore the id field
                if isinstance(field, fields.IDField): continue
                field.contribute_to_model(cls, name)

        # Set collection name to model class that is generated from
        # Model class this name can be user defined or auto generated
        # from model class
        #
        # For example:
        #   class UserCollection:
        #       name = TextField()
        #
        # if user not defined collection name then it will auto generate
        # for this class
        #
        # UserCollection will become user_collection
        setattr(cls, "collection_name", cls._meta.collection_name)

        return cls
