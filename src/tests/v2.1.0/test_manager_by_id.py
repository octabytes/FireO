from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField()


def test_get_by_key_or_id():
    model = MyModel.collection.create(field='test')

    result_by_key_args = MyModel.collection.get(model.key)
    result_by_id_args = MyModel.collection.get(model.id)
    result_by_key_kwargs = MyModel.collection.get(key=model.key)
    result_by_id_kwargs = MyModel.collection.get(id=model.id)

    assert result_by_key_args.id == model.id
    assert result_by_id_args.id == model.id
    assert result_by_key_kwargs.id == model.id
    assert result_by_id_kwargs.id == model.id


def test_get_all_by_key_or_id():
    models = [MyModel.collection.create(field='test') for _ in range(4)]
    keys = [model.key for model in models]
    ids = [model.id for model in models]

    result_by_key_args = list(MyModel.collection.get_all(keys))
    result_by_id_args = list(MyModel.collection.get_all(ids))
    result_by_key_kwargs = list(MyModel.collection.get_all(key_list=keys))
    result_by_id_kwargs = list(MyModel.collection.get_all(id_list=ids))

    assert {model.id for model in result_by_key_args} == set(ids)
    assert {model.id for model in result_by_id_args} == set(ids)
    assert {model.id for model in result_by_key_kwargs} == set(ids)
    assert {model.id for model in result_by_id_kwargs} == set(ids)


def test_update_by_key_or_id():
    models = [MyModel.collection.create(field='test') for _ in range(4)]

    MyModel.collection.update(models[0].key, field='updated by key arg')
    MyModel.collection.update(models[1].id, field='updated by id arg')
    MyModel.collection.update(key=models[2].key, field='updated by key kwarg')
    MyModel.collection.update(id=models[3].id, field='updated by id kwarg')

    for model in models:
        model.refresh()

    assert models[0].field == 'updated by key arg'
    assert models[1].field == 'updated by id arg'
    assert models[2].field == 'updated by key kwarg'
    assert models[3].field == 'updated by id kwarg'


def test_delete_by_key_or_id():
    models = [MyModel.collection.create(field='test') for _ in range(4)]

    MyModel.collection.delete(models[0].key)
    MyModel.collection.delete(models[1].id)
    MyModel.collection.delete(key=models[2].key)
    MyModel.collection.delete(id=models[3].id)

    for model in models:
        model.refresh()

    assert models[0].field is None
    assert models[1].field is None
    assert models[2].field is None
    assert models[3].field is None


def test_delete_all_by_key_or_id():
    models = [MyModel.collection.create(field='test') for _ in range(10)]
    keys = [model.key for model in models]
    ids = [model.id for model in models]

    MyModel.collection.delete_all(keys[0:2])
    MyModel.collection.delete_all(ids[2:4])
    MyModel.collection.delete_all(key_list=keys[4:6])
    MyModel.collection.delete_all(id_list=ids[6:8])

    for model in models:
        model.refresh()

    assert all(model.field is None for model in models[:8])
    assert all(model.field == 'test' for model in models[8:])
