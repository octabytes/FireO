import pytest

from fireo.fields import errors, ListField, NestedModel, TextField
from fireo.models import Model
from fireo.models.errors import ModelSerializingError


class LogAccessField(TextField):
    def db_value(self, val):
        return val + '<saved>'

    def field_value(self, val, model):
        return val + '<loaded>'


class ListTestModel(Model):
    list_field = ListField(nested_field=LogAccessField())
    other_field = TextField()


def test_save_and_load_using_nested_field():
    key = ListTestModel(list_field=['first', 'second']).save().key
    list_field_value = ListTestModel.collection.get(key).list_field

    assert list_field_value == [
        'first<saved><loaded>',
        'second<saved><loaded>'
    ]


def test_save_and_load_empty_list():
    key = ListTestModel(list_field=[]).save().key
    list_field_value = ListTestModel.collection.get(key).list_field

    assert list_field_value == []


def test_save_and_load_none():
    key = ListTestModel(list_field=None, other_field='other').save().key
    list_field_value = ListTestModel.collection.get(key).list_field

    assert list_field_value is None


@pytest.mark.parametrize('nested_field', [str, Model, ListField()])
def test_raise_error_on_unsupported_type(nested_field):
    class BrokenListTestModel(Model):
        list_field = ListField(nested_field=nested_field)

    with pytest.raises(ModelSerializingError) as e:
        BrokenListTestModel(list_field=[]).save()

    assert isinstance(e.value.original_error, errors.AttributeTypeError)