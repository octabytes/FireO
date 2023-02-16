from fireo import db
from fireo.fields import IDField, TextField
from fireo.models import Model


class MyModel(Model):
    id = IDField(include_in_document=True)
    field1 = TextField()


def test_abstract_instance_has_no_id():
    model = MyModel(field1='test', id='test_id')

    model.save()

    doc = db.conn.document(model.key).get()
    doc_dict = doc.to_dict()
    assert model.id == 'test_id'
    assert doc.id == model.id
    assert doc_dict['id'] == model.id
    assert doc_dict['field1'] == model.field1
