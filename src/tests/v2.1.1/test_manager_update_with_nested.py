from fireo.fields import NestedModelField, TextField
from fireo.models import Model


class MyNested(Model):
    field = TextField()


class MyModel(Model):
    nested = NestedModelField(MyNested)
    field = TextField()


def test_update_with_nested():
    model = MyModel()
    model.field = 'field'
    model.save()

    MyModel.collection.update(model.key, nested=MyNested(field='nested_field'))

    model.refresh()

    assert model.nested.field == 'nested_field'
