import pytest

from fireo.fields import TextField, NumberField, NestedModel
from fireo.fields.errors import RequiredField
from fireo.models import Model


class DeepNestedUser(Model):
    name = TextField()
    age = NumberField(default=26)


class DeepNestedStudent(Model):
    uni = TextField(required=True)
    user = NestedModel(DeepNestedUser)


class DeepNestedUni(Model):
    dept = TextField()
    student = NestedModel(DeepNestedStudent)


def test_simple_deep_nested():
    u = DeepNestedUni()
    u.dept = 'Math'
    u.student.uni = 'Abc'
    u.student.user.name = 'Azeem'
    u.save()

    u = DeepNestedUni.collection.get(u.key)

    assert u.dept == 'Math'
    assert u.student.uni == 'Abc'
    assert u.student.user.name == 'Azeem'
    assert u.student.user.age == 26


def test_simple_deep_nested_update():
    u = DeepNestedUni()
    u.dept = 'Math'
    u.student.uni = 'Abc'
    u.student.user.name = 'Azeem'
    u.save()

    u2 = DeepNestedUni()
    u2.student.uni = 'Def'
    u2.student.user.name = 'Arfan'
    u2.update(u.key)

    u3 = DeepNestedUni.collection.get(u2.key)

    assert u3.dept == 'Math'
    assert u3.student.uni == 'Def'
    assert u3.student.user.name == 'Arfan'
    assert u3.student.user.age == 26

class DeepNestedUser2(Model):
    name = TextField()
    age = NumberField(default=26)


class DeepNestedStudent2(Model):
    uni = TextField(required=True)
    user = NestedModel(DeepNestedUser2)


class DeepNestedUni2(Model):
    dept = TextField()
    student = NestedModel(DeepNestedStudent2)


def test_deep_nested_with_required_fields_without_value():
    u = DeepNestedUni2()
    u.dept = 'Math'
    u.student.user.name = 'Azeem'
    u.save()

    u = DeepNestedUni2.collection.get(u.key)

    assert u.dept == 'Math'
    assert u.student.uni is None
    assert u.student.user.name == 'Azeem'
    assert u.student.user.age == 26


class DeepNestedUser3(Model):
    name = TextField()
    age = NumberField(default=26)


class DeepNestedStudent3(Model):
    uni = TextField(required=True)
    user = NestedModel(DeepNestedUser3)


class DeepNestedUni3(Model):
    dept = TextField()
    student = NestedModel(DeepNestedStudent3, required=True)


def test_deep_nested_with_required_fields():
    u = DeepNestedUni3()
    u.dept = 'Math'
    u.student.user.name = 'Azeem'

    with pytest.raises(RequiredField):
        u.save()


class DeepDirectNestedModel(Model):
    name = TextField()


class DirectNestedModel(Model):
    age = NumberField()
    user = NestedModel(DeepDirectNestedModel)


def test_direct_create_nested_model():
    u = DirectNestedModel.collection.create(age=26)

    assert u.age == 26