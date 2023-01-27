import pytest

from fireo.fields import TextField
from fireo.fields.errors import RequiredField
from fireo.models import Model


class TestModel(Model):
    the_field = TextField(required=True)
    other_field = TextField()


def test_field_required_error_message():
    model = TestModel(other_field="other_field")
    with pytest.raises(RequiredField) as e:
        model.save()

    assert str(e.value) == (
        '"the_field" is required for model '
        '<class \'test_field_required_error_message.TestModel\'> '
        'but received no default and no value.'
    )
