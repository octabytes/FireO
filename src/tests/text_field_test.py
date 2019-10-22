import pytest
from fireo.database import db
from fireo.fields import TextField
from fireo.fields.errors import RequiredField
from fireo.models import Model

db.local_connection()


class User(Model):
    name = TextField(max_length=3)


def test_text_max():
    u = User()
    u.name = "123456"
    u.save()

    u2 = User.collection.get(u.key)
    assert u2.name == "123"
