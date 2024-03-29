import pytest

from fireo.fields import TextField
from fireo.fields.errors import RequiredField
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class TestModel(Model):
    the_field = TextField(required=True)
    other_field = TextField()


def test_field_required_error_message():
    model = TestModel(other_field="other_field")
    with pytest.raises(ModelSerializingWrappedError) as e:
        model.save()

    assert isinstance(e.value.original_error, RequiredField)
    assert str(e.value) == (
        "Cannot serialize model 'test_field_required_error_message.TestModel' with "
        f"key 'test_model/{model.id}' due to error in field 'the_field': "
        '"the_field" is required for model <class '
        "'test_field_required_error_message.TestModel'> but received no default and "
        'no value.'
    )
