import pytest

from fireo.models import Model
from fireo.fields.text_field import TextField
from fireo.fields.number_field import NumberField
from fireo.fields.errors import NumberRangeError


def test_fix_issue_48():
    class Person(Model):
        name = TextField(required=True, max_length=10)
        type = NumberField(required=True, int_only=True, range=(1, 2))

    # test TextField
    person = Person.collection.create(name='test', type=1)

    assert person.name == 'test'
    assert person.type == 1

    person.type = 2
    person.update()

    assert person.name == 'test'
    assert person.type == 2

    # test NumberField
    person = Person.collection.create(name='test', type=1)

    assert person.name == 'test'
    assert person.type == 1

    person.name = 'test2'
    person.update()

    assert person.name == 'test2'
    assert person.type == 1

    person.type = 3
    with pytest.raises(NumberRangeError):
        person.update()
