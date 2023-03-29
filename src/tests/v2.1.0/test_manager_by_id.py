from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField()


def test_get_by_id_by_args():
    doc_id = MyModel.collection.create(field='test').id

    doc = MyModel.collection.get(doc_id)

    assert doc.field == 'test'


def test_get_by_id_by_kwargs():
    doc_id = MyModel.collection.create(field='test').id

    doc = MyModel.collection.get(id=doc_id)

    assert doc.field == 'test'