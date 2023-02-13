import pytest

from fireo.fields import NumberField
from fireo.fields.errors import InvalidFieldType
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class User(Model):
    age = NumberField(int_only=True)


def test_num_int():
    u = User()
    u.age = 25
    u.save()

    u2 = User.collection.get(u.key)
    assert u2.age == 25


def test_num_int_wrong():
    with pytest.raises(ModelSerializingWrappedError) as e:
        assert User.collection.create(age=12.34)

    assert isinstance(e.value.original_error, InvalidFieldType)


class User2(Model):
    age = NumberField(float_only=True)


def test_num_float():
    u = User2()
    u.age = 25.23
    u.save()

    u2 = User2.collection.get(u.key)
    assert u2.age == 25.23


def test_num_float_wrong():
    with pytest.raises(ModelSerializingWrappedError) as e:
        assert User2.collection.create(age=12)

    assert isinstance(e.value.original_error, InvalidFieldType)
