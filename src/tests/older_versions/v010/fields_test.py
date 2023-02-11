from datetime import datetime

import fireo
import pytest
from fireo.fields import BooleanField, DateTime, GeoPoint, ListField, MapField, NumberField, TextField, Field
from fireo.fields.errors import InvalidFieldType
from fireo.models import Model
from fireo.models.errors import ModelSerializingError


class Animal(Model):
    name = Field()
    age = Field()


def test_base_field():
    a = Animal()
    a.name = "Bird"
    a.age = 10
    a.save()

    a2 = Animal.collection.get(a.key)
    assert a2.name == a.name
    assert a2.age == a.age

class User(Model):
    field = BooleanField()


def test_bool_field():
    u = User.collection.create(field=True)
    u2 = User.collection.get(u.key)
    assert u2.field == True


def test_bool_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User.collection.create(field="wrong_type")

    assert isinstance(e.value.original_error, InvalidFieldType)


class User2(Model):
    field = DateTime()


def test_datetime_field():
    d = datetime.now()
    u = User2.collection.create(field=d)
    u2 = User2.collection.get(u.key)
    assert u2.field.date() == d.date()
    assert u2.field.ctime() == d.ctime()


def test_datetime_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User2.collection.create(field="wrong_type")

    assert isinstance(e.value.original_error, InvalidFieldType)


class User3(Model):
    field = GeoPoint()


def test_geopoint_field():
    d = fireo.GeoPoint(32.32, 42.32)
    u = User3.collection.create(field=d)
    u2 = User3.collection.get(u.key)
    assert u2.field == d


def test_geopoint_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User3.collection.create(field="wrong_type")

    assert isinstance(e.value.original_error, InvalidFieldType)


class User4(Model):
    field = ListField()


def test_list_field():
    d = ['a','b','c']
    u = User4.collection.create(field=d)
    u2 = User4.collection.get(u.key)
    assert u2.field == d


def test_list_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User4.collection.create(field="wrong_type")

    assert isinstance(e.value.original_error, InvalidFieldType)


class User5(Model):
    field = MapField()


def test_map_field():
    d = {'name': 'Azeem'}
    u = User5.collection.create(field=d)
    u2 = User5.collection.get(u.key)
    assert u2.field == d


def test_map_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User5.collection.create(field="wrong_type")

    assert isinstance(e.value.original_error, InvalidFieldType)


class User6(Model):
    field = NumberField()


def test_num_field():
    d = 123
    u = User6.collection.create(field=d)
    u2 = User6.collection.get(u.key)
    assert u2.field == d


def test_num_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User6.collection.create(field="wrong_type")

    assert isinstance(e.value.original_error, InvalidFieldType)


class User7(Model):
    field = TextField()


def test_text_field():
    d = "Some Text"
    u = User7.collection.create(field=d)
    u2 = User7.collection.get(u.key)
    assert u2.field == d


def test_text_field_e():
    with pytest.raises(ModelSerializingError) as e:
        assert User7.collection.create(field=123)

    assert isinstance(e.value.original_error, InvalidFieldType)
