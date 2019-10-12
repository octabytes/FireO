from fireo.models.errors import AbstractNotInstantiate
from fireo.models.model_meta import ModelMeta


class Model(metaclass=ModelMeta):
    """Provide easy way to handle firestore features

    Model is used to handle firestore operation easily and provide additional features for best
    user experience.

    Example
    -------
    .. code-block:: python

        class User(Model):
            username = TextField(required=True)
            full_name = TextField()
            age = NumberField()

        user = User()
        user.username = "Axeem"
        user.full_name = "Azeem Haider"
        user.age = 25
        user.save()

        # or you can also pass args into constructor
        user = User(username="Axeem", full_name="Azeem", age=25)
        user.save()

        # or you can use it via managers
        user = User.collection.create(username="Axeem", full_name="Azeem", age=25)

    Attributes
    ----------
    _meta : Meta
        Hold all model information like model fields, id, manager etc

    id : str
        Model id if user specify any otherwise it will create automatically from firestore
        and attached with this model

    collection_name : str
        Model name which is saved in firestore if user not specify any then Model class will convert
        automatically in collection name

        For example: UserProfile will be user_profile

    collection : Manager
        Class level attribute through this you can access manager which can be used to save, retrieve or
        update the model in firestore

        Example:
        -------
        .. code-block:: python
            class User(Model):
                name = TextField()

            user = User.collection.create(name="Azeem")

    Methods
    --------
    _get_fields() : dict
        Private method that return values of all attached fields.

    save() : Model instance
        Save the model in firestore collection

    update() : Model instance
        Update the existing document

    Raises
    ------
    AbstractNotInstantiate:
        Abstract model can not instantiate
    """
    id = None
    _meta = None
    collection = None

    def __init__(self, *args, **kwargs):
        # check this is not abstract model otherwise stop creating instance of this model
        if self._meta.abstract:
            raise AbstractNotInstantiate(f'Can not instantiate abstract model {self.__class__.__name__}')
        # pass the model instance if want change in it after save, fetch etc operations
        # otherwise it will return new model instance
        self.__class__.collection.mutable_model(self)

        # Allow users to set fields values direct from the constructor method
        for k, v in kwargs.items():
            setattr(self, k, v)

    # Get all the fields values from meta
    # which are attached with this mode
    # and convert them into corresponding db value
    # return dict {name: value}
    def _get_fields(self):
        """Get Model fields and values

        Retrieve all fields which are attached with Model from `_meta`
        then get corresponding value from model

        Example
        -------
        .. code-block:: python

            class User(Model):
                name = TextField()
                age = NumberField()

            user = User()
            user.name = "Azeem"
            user.age = 25

            # if you call this method `_get_field()` it will return dict{name, val}
            # in this case it will be
            {name: "Azeem", age: 25}

        Returns
        -------
        dict:
            name value dict of model
        """
        return {
            f.name: getattr(self, f.name)
            for f in self._meta.field_list.values()
        }

    @property
    def _id(self):
        """Get Model id

        User can specify model id otherwise it will return None and generate later from
        firestore and attached to model

        Example
        --------
        .. code-block:: python
            class User(Mode):
                user_id = IDField()

            u = User()
            u.user_id = "custom_doc_id"

            # If you call this property it will return user defined id in this case
            print(self._id)  # custom_doc_id

        Returns
        -------
        id : str or None
            User defined id or None
        """
        if self._meta.id is None:
            return None
        name, field = self._meta.id
        return field.get_value(getattr(self, name))

    @_id.setter
    def _id(self, doc_id):
        """Set Model id

        Set user defined id to model otherwise auto generate from firestore and attach
        it to with model

        Example:
        --------
            class User(Model):
                user_id = IDField()
                name = TextField()

            u = User()
            u.name = "Azeem"
            u.save()

            # User not specify any id it will auto generate from firestore
            print(u.user_id)  # xJuythTsfLs

        Parameters
        ----------
        doc_id : str
            Id of the model user specified or auto generated from firestore
        """
        id = 'id'
        if self._meta.id is not None:
            id, _ = self._meta.id
        setattr(self, id, doc_id)

    def save(self):
        """Save Model in firestore collection

        Model classes can saved in firestore using this method

        Example
        -------
        .. code-block:: python
            class User(Model):
                name = TextField()
                age = NumberField()

            u = User(name="Azeem", age=25)
            u.save()

            # print model id
            print(u.id) #  xJuythTsfLs

        Same thing can be achieved from using managers

        See Also
        --------
        fireo.managers.Manager()

        Returns
        -------
        model instance:
            Modified instance of the model contains id etc
        """
        return self.__class__.collection.create(**self._get_fields())

    def update(self):
        """Update the existing document

        Update document without overriding it. You can update selected fields.

        Examples
        --------
        .. code-block:: python
            class User(Model):
                name = TextField()
                age = NumberField()

            u = User.collection.create(name="Azeem", age=25)
            id = u.id

            # update this
            user = User.collection.get(id)
            user.name = "Arfan"
            user.update()

            print(user.name)  # Arfan
            print(user.age)  # 25
        """
        return self.__class__.collection.update(**self._get_fields())

