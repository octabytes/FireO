from fireo.database import db
from fireo.fields import TextField
from fireo.models import Model


db.local_connection()


class User(Model):
    name = TextField()


def test_simple_save():
    u1 = User()
    u1.name = 'test_simple_save'
    u1.save()

    u2 = User.collection.get(u1.key)
    assert u1.id == u2.id
    assert u1.name == u2.name
    assert u1.key == u2.key


def test_save_and_save():
    u1 = User()
    u1.name = 'test_save_and_save'
    u1.save()

    u1.name = "change_test_save_and_save"
    u1.save()

    u2 = User.collection.get(u1.key)
    assert u1.id == u2.id
    assert u1.name == u2.name
    assert u1.key == u2.key


def test_save_get_save():
    u1 = User()
    u1.name = 'test_save_get_save'
    u1.save()

    u2 = User.collection.get(u1.key)
    u2.name = 'change_test_save_get_save'
    u2.save()

    u3 = User.collection.get(u2.key)
    assert u3.id == u2.id
    assert u3.name == u2.name
    assert u3.key == u2.key


def test_create():
    u = User.collection.create(name='test_create')

    assert u.name == 'test_create'


def test_create_get():
    u1 = User.collection.create(name='test_create_get')
    u2 = User.collection.get(u1.key)

    assert u1.id == u2.id
    assert u1.key == u2.key
    assert u1.name == u2.name


def test_create_save():
    u = User.collection.create(name='test_create_save')
    u.name = 'change_test_create_save'
    u.save()

    assert u.name == 'change_test_create_save'


def test_create_save_get():
    u1 = User.collection.create(name='test_create_save_get')
    u1.name = 'change_test_create_save_get'
    u1.save()

    u2 = User.collection.get(u1.key)
    assert u1.id == u2.id
    assert u1.key == u2.key
    assert u1.name == u2.name
    assert u2.name == 'change_test_create_save_get'


def test_create_get_save():
    u1 = User.collection.create(name='test_create_get_save')

    u2 = User.collection.get(u1.key)
    u2.name = 'change_test_create_get_save'
    u2.save()

    assert u2.name == 'change_test_create_get_save'