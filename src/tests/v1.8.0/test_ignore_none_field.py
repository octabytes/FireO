from fireo import db
from fireo.fields import NestedModelField, TextField
from fireo.models import Model


class NestedIgnoreNoneModel(Model):
    class Meta:
        ignore_none_field = True

    field1 = TextField()
    field2 = TextField(default='default')


class IgnoreNoneModel(Model):
    class Meta:
        ignore_none_field = True

    field1 = TextField()
    field2 = TextField(default='default')
    nested = NestedModelField(NestedIgnoreNoneModel)


def test_ignore_default_none_on_create():
    model = IgnoreNoneModel().save()

    doc_dict = db.conn.collection(IgnoreNoneModel.collection_name).document(model.id).get().to_dict()

    assert doc_dict == {'field2': 'default', 'nested': {'field2': 'default'}}


def test_not_ignore_not_default_none_on_update():
    model = IgnoreNoneModel().save()
    model.nested.field1 = None
    model.save()

    doc_dict = db.conn.collection(IgnoreNoneModel.collection_name).document(model.id).get().to_dict()

    assert doc_dict == {
        'field2': 'default',
        'nested': {
            'field1': None,
            'field2': 'default',
        },
    }


class NestedNotIgnoreNoneModel(Model):
    class Meta:
        ignore_none_field = False

    field1 = TextField()
    field2 = TextField(default='default')


class NotIgnoreNoneModel(Model):
    class Meta:
        ignore_none_field = False

    field1 = TextField()
    field2 = TextField(default='default')
    nested = NestedModelField(NestedIgnoreNoneModel)


def test_not_ignore_default_none_on_create():
    model = NotIgnoreNoneModel().save()

    doc_dict = db.conn.collection(NotIgnoreNoneModel.collection_name).document(model.id).get().to_dict()

    assert doc_dict == {
        'field1': None,
        'field2': 'default',
        'nested': {
            'field1': None,
            'field2': 'default',
        }
    }
