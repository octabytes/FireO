from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField()
    field2 = TextField()


def test_update_from_manager_by_key():
    key = MyModel.collection.create(field='test').key

    MyModel.collection.update(key=key, field2='test2')

    doc = MyModel.collection.get(key)

    assert doc.field == 'test'
    assert doc.field2 == 'test2'


def test_update_from_manager_by_instance():
    model = MyModel.collection.create(field='test')

    MyModel.collection.update(mutable_instance=model, field2='test2')

    updated = MyModel.collection.get(model.key)

    assert model.field == updated.field == 'test'
    assert model.field2 == updated.field2 == 'test2'
