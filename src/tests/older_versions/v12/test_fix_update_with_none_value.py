import pytest

from fireo.models import Model
from fireo.fields.text_field import TextField
from fireo.fields.number_field import NumberField
from fireo.fields.errors import NumberRangeError
from fireo.models.errors import ModelSerializingWrappedError


def test_fix_issue_48():
    class Person(Model):
        first_name = TextField(required=True, max_length=10)
        last_name = TextField(max_length=10)
        type = NumberField(required=True, int_only=True, range=(1, 2))

    # test TextField
    person = Person.collection.create(first_name='test', type=1)

    assert person.first_name == 'test'
    assert person.type == 1

    person.type = 2
    person.update()

    assert person.first_name == 'test'
    assert person.type == 2

    # test NumberField
    person = Person.collection.create(first_name='test', type=1)

    assert person.first_name == 'test'
    assert person.type == 1

    person.first_name = 'test2'
    person.update()

    assert person.first_name == 'test2'
    assert person.type == 1

    person.type = 3
    with pytest.raises(ModelSerializingWrappedError) as e:
        person.update()

    assert isinstance(e.value.original_error, NumberRangeError)
