from fireo.managers import managers
from fireo.models import fields
from fireo.utils import utils

"""
Create modified instance of Model 

Add meta attribute to each Model which holds all the information about Model Fields
Which help for further use of these Fields
"""


class ModelMeta(type):
    def __new__(mcs, name, base, attrs):
        cls = super().__new__(mcs, name, base, attrs)

        if 'Meta' not in attrs:
            cls.Meta = None

        """
            Meta class holding all your Model fields and add them back to your 
            Model class inside meta attribute
        """
        class Meta:
            field_list = {}
            id = None

            def __init__(self, model):
                self.collection_name = utils.collection_name(cls.__name__)

            if 'collection' not in cls.__dict__:
                manager = managers.Manager()
                manager.contribute_to_model(cls)

            # Add model id
            def add_model_id(self, field):
                self.id = (field.name, field)

            # Add each single field into Meta fields into this Model
            def add_field(self, field):
                self.field_list[field.name] = field

            def get_field_by_column_name(self, name):
                for field in self.field_list.values():
                    if name in [field.name, field.db_column_name]:
                        return field
                raise AttributeError(f'Field {name} not found')


        # instance of Meta class and set it to
        # Model class as _meta attribute
        _meta = Meta(cls)
        setattr(cls, '_meta', _meta)

        # get list of attribute from Model
        for name, field in cls.__dict__.items():
            if isinstance(field, fields.Field):
                field.contribute_to_model(cls, name)

        setattr(cls, "collection_name", cls._meta.collection_name)

        return cls
