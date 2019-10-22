from fireo import models as mdl
from fireo.database import db

db.local_connection()


class User(mdl.Model):
    id = mdl.IDField()
    name = mdl.TextField()


def test_id():
    u = User()
    u.id = 'test_id_field'
    u.name = 'testing_id_field'
    u.save()

    u2 = User.collection.get(u.key)
    assert u2.id == u.id
    assert u2.name == u.name
    assert u2.key == u.key


def test_without_id():
    u1 = User()
    u1.name = 'test_without_id'
    u1.save()

    u2 = User.collection.get(u1.key)
    assert u1.id == u2.id
    assert u1.name == u2.name
    assert u1.key == u2.key


class Student(mdl.Model):
    user_id = mdl.IDField()
    name = mdl.TextField()


def test_id_with_different_name():
    s1 = Student()
    s1.user_id = 'test_id_with_different_name'
    s1.name = 'testing_id_with_different_name'
    s1.save()

    s2 = Student.collection.get(s1.key)
    assert s1.user_id == s2.user_id
    assert s1.name == s2.name
    assert s1.key == s2.key

    assert s1.id is None
    assert s2.id is None


def test_id_without_value():
    s1 = Student()
    s1.name = 'testing_id_with_different_name'
    s1.save()

    s2 = Student.collection.get(s1.key)
    assert s1.user_id == s2.user_id
    assert s1.name == s2.name
    assert s1.key == s2.key

    assert s1.id is None
    assert s2.id is None


class Employee(mdl.Model):
    name = mdl.TextField()


def test_without_id_field():
    e1 = Employee()
    e1.name = 'test_without_id_field'
    e1.save()

    e2 = Employee.collection.get(e1.key)
    assert e1.id == e2.id
    assert e1.name == e2.name
    assert e1.key == e2.key


def test_without_id_field_but_giving_id():
    e1 = Employee()
    e1.id = 'test_without_id_but_giving_id'
    e1.name = 'test_without_id_but_give_some_id'
    e1.save()

    assert e1.id != 'test_without_id_but_giving_id'

    e2 = Employee.collection.get(e1.key)
    assert e2.id != 'test_without_id_but_giving_id'
    assert e1.name == e2.name
    assert e1.key == e2.key
