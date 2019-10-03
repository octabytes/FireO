from fireo.models import fields

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
            fields = {}

            # Add each single field into Meta fields
            def add_field(self, field):
                self.fields[field.name] = field

        # instance of Meta class and set it to
        # Model class as _meta attribute
        meta = Meta()
        setattr(cls, 'meta', meta)

        # get list of attribute from Model
        for name, attr in cls.__dict__.items():
            if isinstance(attr, fields.Field):
                attr.contribute_to_model(cls, name)

        return cls
