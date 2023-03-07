from fireo.fields import TextField
from fireo.models import Model
from fireo.models.model_meta import Meta, ModelMeta


class MyMeta(Meta):
    supported_fields = [*Meta.supported_fields, 'my_field']
    inherited_fields = [*Meta.inherited_fields, 'my_field']

    my_field = 'my field default'


class MyModelMeta(ModelMeta):
    _meta_cls = MyMeta


class BaseModelWithDefault(Model, metaclass=MyModelMeta):
    class Meta:
        abstract = True


class ModelWithDefault(BaseModelWithDefault):
    field = TextField()


class ModelWithOverride(BaseModelWithDefault):
    field = TextField()

    class Meta:
        my_field = 'new'


class BaseModelWithOverride(Model, metaclass=MyModelMeta):
    class Meta:
        abstract = True
        my_field = 'new'


class ModelWithInherit(BaseModelWithOverride):
    field = TextField()


def test_meta_inheritance():
    assert ModelWithDefault._meta.my_field == 'my field default'
    assert ModelWithOverride._meta.my_field == 'new'
    assert ModelWithInherit._meta.my_field == 'new'
