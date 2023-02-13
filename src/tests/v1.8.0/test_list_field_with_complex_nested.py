import pytest

from fireo.fields import ListField, TextField
from fireo.fields.nested_model_field import NestedModelField
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class Deep1NestedModel(Model):
    field = TextField()


class Deep2NestedModel(Model):
    nested = NestedModelField(Deep1NestedModel)


class Deep3ListNestedModel(Model):
    nested = ListField(nested_field=NestedModelField(Deep2NestedModel))


class Deep4NestedModel(Model):
    nested = NestedModelField(Deep3ListNestedModel)


@pytest.mark.parametrize('nested_field,nested_value', [
    (TextField(),
     ['str']),
    (NestedModelField(Deep1NestedModel),
     [dict(field='str')]),
    (NestedModelField(Deep2NestedModel),
     [dict(nested=dict(field='str'))]),
    (NestedModelField(Deep3ListNestedModel),
     [dict(nested=[dict(nested=dict(field='str'))])]),
    (NestedModelField(Deep4NestedModel),
     [dict(nested=dict(nested=[dict(nested=dict(field='str'))]))]),
])
def test_save_and_load_with(nested_field, nested_value):
    class NestedListTestModel(Model):
        simple_field = TextField()
        list_field = ListField(nested_field=nested_field)

    dict_value = {
        'simple_field': 'simple',
        'list_field': nested_value,
    }

    obj = NestedListTestModel.from_dict(dict_value)
    obj.save()

    db_obj = NestedListTestModel.collection.get(obj.key)
    new_dict_value = db_obj.to_dict()
    new_dict_value.pop('id')
    new_dict_value.pop('key')
    assert new_dict_value == dict_value


def test_error_message_has_list_index():
    class NestedModel(Model):
        field = TextField(required=True)
        field2 = TextField(required=True)

    class TestModel(Model):
        list_field = ListField(nested_field=NestedModelField(NestedModel))

    with pytest.raises(ModelSerializingWrappedError) as e:
        TestModel.from_dict(dict(list_field=[dict(field='str')])).save()

    assert str(e.value) == (
        'Cannot serialize model '
        "'test_list_field_with_complex_nested.test_error_message_has_list_index.<locals>.TestModel' "
        "with key 'test_model/@temp_doc_id' due to error in field "
        '\'list_field[0].field2\': "field2" is required for model <class '
        "'test_list_field_with_complex_nested.test_error_message_has_list_index.<locals>.NestedModel'> "
        'but received no default and no value.'
    )
