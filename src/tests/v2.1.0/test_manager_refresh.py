from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField()
    field2 = TextField()


def test_refresh_from_manager():
    model = MyModel.collection.create(field='test')
    MyModel.collection.update(model.key, field2='test2')

    MyModel.collection.refresh(model)

    assert model.field == 'test'
    assert model.field2 == 'test2'

