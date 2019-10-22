import pytest
from fireo.database import db
from fireo.fields import TextField, NumberField
from fireo.models import Model
from fireo.models.errors import AbstractNotInstantiate, NonAbstractModel

db.local_connection()

class User(Model):
    name = TextField()

    class Meta:
        abstract = True


def test_abstract_not_instantiate():
    with pytest.raises(AbstractNotInstantiate):
        u = User()


class Student(User):
    age = NumberField()


def test_abstract_model():
    s = Student()
    s.name = "Arfan"
    s.age = 27
    s.save()

    s2 = Student.collection.get(s.key)

    assert s2.name == 'Arfan'
    assert s2.age == 27


def test_extend_from_non_abstract():
    with pytest.raises(NonAbstractModel):
        class User2(Model):
            name = TextField()

        class Student2(User2):
            age = NumberField()
