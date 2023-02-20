from google.cloud.firestore_v1.field_path import FieldPath

from fireo import db
from fireo.fields import IDField, TextField
from fireo.models import Model


class MyModel(Model):
    custom_id = IDField(include_in_document=True)
    field = TextField(column_name='alias')


def test_filter_by_id_field_in_doc():
    db.conn.collection(MyModel.collection_name).add({'custom_id': '111', 'alias': 'value'}, '222')

    assert MyModel.collection.filter('custom_id', '==', '111').get().field == 'value'
    assert MyModel.collection.filter('_id', '==', '222').get().field == 'value'
    assert MyModel.collection.filter(FieldPath.document_id(), '==', '222').get().field == 'value'
