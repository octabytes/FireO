from fireo.fields import NestedModel, TextField
from fireo.models import Model


class Deep0Model(Model):
    my_nested_field = TextField()
    my_nested_field2 = TextField()


class Deep1Model(Model):
    my_field = TextField()
    my_field2 = TextField()
    my_nested_model = NestedModel(Deep0Model, required=True)


class Deep2Model(Model):
    my_field = TextField()
    my_field2 = TextField()
    my_nested_model = NestedModel(Deep1Model, required=True)


def test_update_first_level_in_model_with_nested():
    model = Deep1Model.from_dict(dict(
        my_field='value',
        my_field2='value2',
        my_nested_model=dict(my_nested_field='my_nested_field')
    ))
    model.save()

    model_from_db = Deep1Model.collection.get(model.key)

    # this works
    assert model_from_db.my_field == 'value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'my_nested_field'

    Deep1Model(my_field='new value').update(model.key)
    model_from_db = Deep1Model.collection.get(model.key)

    assert model_from_db.my_field == 'new value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'my_nested_field'


def test_update_nested():
    model = Deep1Model.from_dict(dict(
        my_field='value',
        my_field2='value2',
        my_nested_model=dict(
            my_nested_field='my_nested_field',
            my_nested_field2='my_nested_field2',
        )
    ))
    model.save()

    Deep1Model(
        my_field='new value',
        my_nested_model=dict(my_nested_field='new nested'),
    ).update(model.key)
    model_from_db = Deep1Model.collection.get(model.key)

    assert model_from_db.my_field == 'new value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'new nested'
    assert model_from_db.my_nested_model.my_nested_field2 == 'my_nested_field2'


def test_update_deep_nested():
    model = Deep2Model.from_dict(
        dict(
            my_field='value',
            my_field2='value2',
            my_nested_model=dict(
                my_field='value',
                my_field2='value2',
                my_nested_model=dict(
                    my_nested_field='my_nested_field',
                )
            )
        )
    )
    model.save()

    Deep2Model(
        my_field='new value',
        my_nested_model=dict(
            my_field='new value',
            my_nested_model=dict(
                my_nested_field='new nested',
            )
        )
    ).update(model.key)

    model_from_db = Deep2Model.collection.get(model.key)

    assert model_from_db.my_field == 'new value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_field == 'new value'
    assert model_from_db.my_nested_model.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_model.my_nested_field == 'new nested'


def test_updated_nested_with_none():
    model = Deep1Model.from_dict(dict(
        my_field='value',
        my_field2='value2',
        my_nested_model=dict(
            my_nested_field='my_nested_field',
            my_nested_field2='my_nested_field2',
        )
    ))
    model.save()

    model_to_update = Deep1Model()
    model_to_update.my_nested_model.my_nested_field2 = None
    model_to_update.update(model.key)

    model_from_db = Deep1Model.collection.get(model.key)

    assert model_from_db.my_field == 'value'
    assert model_from_db.my_field2 == 'value2'
    assert model_from_db.my_nested_model.my_nested_field == 'my_nested_field'
    assert model_from_db.my_nested_model.my_nested_field2 is None
