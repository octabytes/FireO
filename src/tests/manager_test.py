import pytest
from fireo.database import db
from fireo.fields import TextField
from fireo.managers.managers import ManagerError
from fireo.models import Model

db.local_connection()

class User(Model):
    name = TextField()


def test_manger_not_access_from_instance():
    u = User()

    with pytest.raises(ManagerError):
        u.collection.get('key/value')


class Student(Model):
    name = TextField()

    class Meta:
        abstract = True


def test_manager_not_access_abstract():
    with pytest.raises(ManagerError):
        Student.collection.get('key/value')