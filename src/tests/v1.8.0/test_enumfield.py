from enum import Enum

import pytest
from google.cloud.firestore_v1 import DocumentReference

from fireo import db
from fireo.fields.enum_field import EnumField
from fireo.fields.errors import AttributeTypeError
from fireo.models import Model


class MyEnum(Enum):
    FIRST = 'the first'
    SECOND = 'the second'
    THIRD = 'the third'


class MyEnumModel(Model):
    my_enum = EnumField(enum=MyEnum)


def test_serialize_and_deserialize_to_and_from_enum():
    key = MyEnumModel(my_enum=MyEnum.SECOND).save().key
    from_db: MyEnumModel = MyEnumModel.collection.get(key)

    assert from_db.my_enum is MyEnum.SECOND


def test_raise_error_on_wrong_field_value():
    _, ref = db.conn.collection(MyEnumModel.collection_name).add({'my_enum': 'wrong'})
    with pytest.raises(ValueError):
        MyEnumModel.collection.get(ref.path)


def test_raise_error_on_wrong_attribute_value():
    with pytest.raises(AttributeTypeError):
        EnumField(enum=object())
