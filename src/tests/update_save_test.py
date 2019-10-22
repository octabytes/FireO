from fireo.database import db
from fireo.fields import TextField, IDField
from fireo.models import Model


db.local_connection()


class User(Model):
    name = TextField()
    address = TextField()


def test_save_update():
    u = User(name="test_save_update")
    u.address = 'test_save_update_address'
    u.save()

    u2 = User.collection.get(u.key)
    u2.name = 'update_test_save_update'
    u2.update()

    u3 = User.collection.get(u.key)
    assert u3.name == 'update_test_save_update'
    assert u3.address == 'test_save_update_address'


class Student(Model):
    id = IDField()
    name = TextField()
    address = TextField()


def test_save_update_with_id():
    u = User()
    u.id = 'test_save_update_with_id'
    u.name="test_save_update_with_id"
    u.address = 'test_save_update_with_id_address'
    u.save()

    u2 = User.collection.get(u.key)
    u2.name = 'update_test_save_update_with_id'
    u2.update()

    u3 = User.collection.get(u.key)
    assert u3.name == 'update_test_save_update_with_id'
    assert u3.address == 'test_save_update_with_id_address'
    assert u3.id == 'test_save_update_with_id'


def test_save_update_without_value():
    u = User()
    u.name="test_save_update_without_value"
    u.address = 'test_save_update_without_value_address'
    u.save()

    u2 = User.collection.get(u.key)
    u2.name = 'update_test_save_update_without_value'
    u2.update()

    u3 = User.collection.get(u.key)
    assert u3.name == 'update_test_save_update_without_value'
    assert u3.address == 'test_save_update_without_value_address'
    assert u3.id == u.id


class Employee(Model):
    user_id = IDField()
    name = TextField()
    address = TextField()


def test_save_update_different_name():
    u = Employee()
    u.user_id = 'test_save_update_different_name'
    u.name = "test_save_update_different_name"
    u.address = 'test_save_update_different_name_address'
    u.save()

    u2 = Employee.collection.get(u.key)
    u2.name = 'update_test_save_update_different_name'
    u2.update()

    u3 = Employee.collection.get(u.key)
    assert u3.name == 'update_test_save_update_different_name'
    assert u3.address == 'test_save_update_different_name_address'
    assert u3.user_id == u.user_id
    assert u3.id is None


def test_save_update_with_value():
    u = Employee()
    u.id = 'test_save_update_with_value'
    u.name = "test_save_update_with_value"
    u.address = 'test_save_update_with_value_address'
    u.save()

    u2 = Employee.collection.get(u.key)
    u2.name = 'update_test_save_update_with_value'
    u2.update()

    u3 = Employee.collection.get(u.key)
    assert u3.name == 'update_test_save_update_with_value'
    assert u3.address == 'test_save_update_with_value_address'
    assert u3.user_id == u.user_id
    assert u3.id != 'test_save_update_with_value'