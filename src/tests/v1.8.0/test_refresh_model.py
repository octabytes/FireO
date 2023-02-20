from google.cloud import firestore

from fireo import db
from fireo.fields import NestedModelField, TextField
from fireo.models import Model


class MyNestedModel(Model):
    field1 = TextField()
    field2 = TextField()
    field3 = TextField()


class MyModel(Model):
    field1 = TextField()
    field2 = TextField()
    field3 = TextField()
    nested = NestedModelField(MyNestedModel)


def test_changed_in_db():
    model = MyModel()
    model.field1 = "value1"
    model.field2 = "value2"
    model.field3 = "value3"
    model.nested.field1 = "nested_value1"
    model.nested.field2 = "nested_value2"
    model.nested.field3 = "nested_value3"
    model.save()

    db.conn.collection(MyModel.collection_name).document(model.id).update({
        "field1": firestore.DELETE_FIELD,
        "field2": "changed_value2",
        "nested.field1": firestore.DELETE_FIELD,
        "nested.field2": "changed_nested_value2",
    })

    model.refresh()

    assert model.field1 is None
    assert model.field2 == "changed_value2"
    assert model.field3 == "value3"
    assert model.nested.field1 is None
    assert model.nested.field2 == "changed_nested_value2"
    assert model.nested.field3 == "nested_value3"

