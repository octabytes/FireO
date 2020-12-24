import pytest
from fireo.database import db
from fireo.fields import TextField
from fireo.fields.errors import RequiredField, UnSupportedAttribute
from fireo.models import Model
from fireo.utils import utils


class User1(Model):
    name = TextField(default="default_value")


def test_default_value():
    u = User1()
    u.save()

    u2 = User1.collection.get(u.key)
    assert u2.name == 'default_value'


class User2(Model):
    address = TextField()
    name = TextField(required=True)


def test_required_value():
    u = User2()
    u.address = "City 123"

    with pytest.raises(RequiredField):
        u.save()


class User3(Model):
    name = TextField(column_name="fireo_column")


def test_column_name():
    u = User3()
    u.name = 'db_column_name_test'
    u.save()

    doc = db.conn.collection('user3').document(utils.get_id(u.key)).get()
    doc_dict = doc.to_dict()

    assert doc_dict['fireo_column'] == 'db_column_name_test'


class User4(Model):
    name = TextField(not_supported="Un supported attribute")


def test_un_supported_attribute():
    u = User4()
    u.name = 'Azeem'

    with pytest.raises(UnSupportedAttribute):
        u.save()