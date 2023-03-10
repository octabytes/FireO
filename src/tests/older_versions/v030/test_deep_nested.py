import pytest

from fireo.fields import NestedModel, NumberField, TextField
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class DeepNestedUser(Model):
    name = TextField()
    age = NumberField(default=26)


class DeepNestedStudent(Model):
    uni = TextField(required=True)
    user = NestedModel(DeepNestedUser, required=True)


class DeepNestedUni(Model):
    dept = TextField()
    student = NestedModel(DeepNestedStudent, required=True)


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
    user = NestedModel(DeepNestedUser2, required=True)


class DeepNestedUni2(Model):
    dept = TextField()
    student = NestedModel(DeepNestedStudent2, required=True)


def test_deep_nested_with_required_fields_without_value():
    u = DeepNestedUni2()
    u.dept = 'Math'
    u.student.user.name = 'Azeem'

    with pytest.raises(ModelSerializingWrappedError) as e:
        u.save()

    assert str(e.value) == (
        "Cannot serialize model 'test_deep_nested.DeepNestedUni2' with key "
        f"'deep_nested_uni2/{u.id}' due to error in field 'student.uni': "
        '"uni" is required for model <class \'test_deep_nested.DeepNestedStudent2\'> '
        'but received no default and no value.'
    )


class DeepNestedUser3(Model):
    name = TextField()
    age = NumberField(default=26)


class DeepNestedStudent3(Model):
    uni = TextField(required=True)
    user = NestedModel(DeepNestedUser3, required=True)


class DeepNestedUni3(Model):
    dept = TextField()
    student = NestedModel(DeepNestedStudent3, required=True)


def test_deep_nested_with_required_fields():
    u = DeepNestedUni3()
    u.dept = 'Math'
    u.student.user.name = 'Azeem'

    with pytest.raises(ModelSerializingWrappedError) as e:
        u.save()
    assert str(e.value) == (
        "Cannot serialize model 'test_deep_nested.DeepNestedUni3' with key "
        f"'deep_nested_uni3/{u.id}' due to error in field 'student.uni': "
        '"uni" is required for model <class \'test_deep_nested.DeepNestedStudent3\'> '
        'but received no default and no value.'
    )


class DeepDirectNestedModel(Model):
    name = TextField()


class DirectNestedModel(Model):
    age = NumberField()
    user = NestedModel(DeepDirectNestedModel)


def test_direct_create_nested_model():
    u = DirectNestedModel.collection.create(age=26)

    assert u.age == 26
