import pytest
from fireo.database import db
from fireo.fields import TextField, NumberField, IDField
from fireo.fields.errors import MissingFieldOptionError, FieldNotFound
from fireo.models import Model
from fireo.models.errors import UnSupportedMeta
from fireo.utils import utils


def test_collection_name():
    class User(Model):
        name = TextField()

        class Meta:
            collection_name = 'collection_name_test'

    u = User.collection.create(name="Arfan")

    doc = db.conn.collection('collection_name_test').document(utils.get_id(u.key)).get()

    assert doc.id == utils.get_id(u.key)


def test_missing_fields():
    class User1(Model):
        name = TextField()
        age = NumberField()

        class Meta:
            missing_field = 'merge'

    u = User1.collection.create(name="Arfan", age=27)

    class User1(Model):
        name = TextField()

        class Meta:
            missing_field = 'merge'

    u2 = User1.collection.get(u.key)

    assert u2.name == u.name
    assert u2.age == u.age


def test_missing_fields_ignore():
    class User2(Model):
        name = TextField()
        age = NumberField()

        class Meta:
            missing_field = 'ignore'

    u = User2.collection.create(name="Arfan", age=27)

    class User2(Model):
        name = TextField()
        class Meta:
            missing_field = 'ignore'

    u2 = User2.collection.get(u.key)

    assert u2.name == u.name
    with pytest.raises(AttributeError):
        assert u2.age is None


def test_missing_fields_err():
    class User3(Model):
        name = TextField()
        age = NumberField()

        class Meta:
            missing_field = 'raise_error'

    u = User3.collection.create(name="Arfan", age=27)

    class User3(Model):
        name = TextField()

        class Meta:
            missing_field = 'raise_error'

    with pytest.raises(FieldNotFound):
        User3.collection.get(u.key)


def test_missing_fields_not_supported():
    with pytest.raises(MissingFieldOptionError):
        class User4(Model):
            name = TextField()
            age = NumberField()

            class Meta:
                missing_field = 'unknown'


def test_unsupported_meta_field():
    with pytest.raises(UnSupportedMeta):
        class User5(Model):
            name = TextField()

            class Meta:
                unknow = 'something'
