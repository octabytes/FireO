from fireo import db
from fireo.fields import IDField, TextField
from fireo.models import Model


def test_id_with_include_in_document_added_as_field():
    class MyModel(Model):
        id = IDField(include_in_document=True)
        field1 = TextField()

    model = MyModel(field1='test', id='test_id')

    model.save()

    doc = db.conn.document(model.key).get()
    doc_dict = doc.to_dict()
    assert model.id == 'test_id'
    assert doc.id == model.id
    assert doc_dict['id'] == model.id
    assert doc_dict['field1'] == model.field1


def test_populate_id_field_in_document_on_create():
    class MyModel(Model):
        id = IDField(include_in_document=True)
        field1 = TextField()

    model = MyModel(field1='test')
    model.save()

    doc = db.conn.document(model.key).get()
    doc_dict = doc.to_dict()
    assert model.id == doc.id
    assert doc_dict.get('id') == doc.id


def test_populate_custom_id_field_in_document_on_create():
    class MyModel(Model):
        custom_id = IDField(include_in_document=True)
        field1 = TextField()

    model = MyModel(field1='test')
    model.save()

    doc = db.conn.document(model.key).get()
    doc_dict = doc.to_dict()
    assert model.custom_id == doc.id
    assert doc_dict.get('custom_id') == doc.id


def test_populate_required_custom_id_field_in_document_on_create():
    class MyModel(Model):
        custom_id = IDField(include_in_document=True, required=True)
        field1 = TextField()

    model = MyModel(field1='test')
    model.save()

    doc = db.conn.document(model.key).get()
    doc_dict = doc.to_dict()
    assert model.custom_id == doc.id
    assert doc_dict.get('custom_id') == doc.id
