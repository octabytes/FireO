from fireo.models import Model
from fireo.fields.text_field import TextField
from fireo.fields.number_field import NumberField


def test_fix_issue_48():
    class Person(Model):
        name = TextField(required=True, max_length=10)
        type = NumberField(required=True, int_only=True)


    person = Person.collection.create(name="test", type=1)

    assert person.name == 'test'
    assert person.type == 1

    person.type = 123
    person.update()

    assert person.name == 'test'
    assert person.type == 123
