from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    name = TextField()

    class Meta:
        collection_name = 'my-model'


def test_refresh_deleted():
    model = MyModel.collection.create(name='test')

    MyModel.collection.delete(model.key)

    model.refresh()
    assert model.name is None
