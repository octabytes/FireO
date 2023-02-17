import fireo
from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField()


def test_set_id_on_batch_create():
    model = MyModel(field='test')

    with fireo.batch() as batch:
        model.save(batch=batch)

    assert model.id is not None
    assert MyModel.collection.get(model.key).field == 'test'
