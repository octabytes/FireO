from fireo.fields import NestedModel, TextField
from fireo.models import Model


class MyNestedModel(Model):
    my_nested_field = TextField()
    my_nested_field2 = TextField()


class MyModel(Model):
    my_field = TextField()
    my_field2 = TextField()
    my_nested_model = NestedModel(MyNestedModel)


def test_update():
    model = MyModel.from_dict(dict(
        my_field='value',
        my_field2='value2',
        my_nested_model=dict(my_nested_field='my_nested_field')
    ))
    model.save()

    model_from_db = MyModel.collection.get(model.key)

    # this works
    assert model_from_db.my_field == 'value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'my_nested_field'

    MyModel(my_field='new value').update(model.key)
    model_from_db = MyModel.collection.get(model.key)

    assert model_from_db.my_field == 'new value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'my_nested_field'


def test_updated_nested_with_none():
    model = MyModel.from_dict(dict(
        my_field='value',
        my_field2='value2',
        my_nested_model=dict(
            my_nested_field='my_nested_field',
            my_nested_field2='my_nested_field2',
        )
    ))
    model.save()

    model_to_update = MyModel()
    model_to_update.my_nested_model.my_nested_field2 = None
    model_to_update.update(model.key)

    model_from_db = MyModel.collection.get(model.key)

    assert model_from_db.my_field == 'value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'my_nested_field'
    assert model_from_db.my_nested_model.my_nested_field2 is None

