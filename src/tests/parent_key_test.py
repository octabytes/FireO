from fireo import models as mdl
from fireo.database import db

db.local_connection()

class User(mdl.Model):
    id = mdl.IDField()
    name = mdl.TextField()


class Student(mdl.Model):
    id = mdl.IDField()
    address = mdl.TextField()


def test_parent_key_with_id_field():
    u = User()
    u.id = 'test_parent_key_with_id_field'
    u.name = 'testing parent key with id field'
    u.save()

    s1 = Student(parent=u.key)
    s1.id = 'student_id_in_test_parent_key'
    s1.address = 'testing parent student key'
    s1.save()

    s2 = Student.collection.get(s1.key)
    assert s1.id == s2.id
    assert s1.key == s2.key


class User1(mdl.Model):
    user_id = mdl.IDField()
    name = mdl.TextField()


class Student1(mdl.Model):
    student_id = mdl.IDField()
    address = mdl.TextField()


def test_parent_key_with_custom_field():
    u = User1()
    u.user_id = 'test_parent_key_with_custom_field'
    u.name = 'testing parent key with_custom_field'
    u.save()

    s1 = Student1(parent=u.key)
    s1.student_id = 'student_id_test_parent_key_with_custom_field'
    s1.address = 'testing parent student keywith_custom_field'
    s1.save()

    s2 = Student1.collection.get(s1.key)
    assert s1.student_id == s2.student_id
    assert s1.key == s2.key

    assert s1.id is None
    assert s2.id is None


def test_parent_key_custom_field_without_value():
    u = User1()
    u.name = 'testing parent key with_custom_field'
    u.save()

    s1 = Student1(parent=u.key)
    s1.address = 'testing parent student keywith_custom_field'
    s1.save()

    s2 = Student1.collection.get(s1.key)
    assert s1.student_id == s2.student_id
    assert s1.key == s2.key

    assert s1.id is None
    assert s2.id is None


def test_parent_key_without_value():
    u = User()
    u.id = 'test_parent_key_without_value'
    u.name = 'testing parent key without value'
    u.save()

    s1 = Student(parent=u.key)
    s1.id = 'student_id_in_test_parent_key_without_value'
    s1.address = 'testing parent student key without value'
    s1.save()

    s2 = Student.collection.get(s1.key)
    assert s1.id == s2.id
    assert s1.key == s2.key


class Company(mdl.Model):
    name = mdl.TextField()


class Employee(mdl.Model):
    address = mdl.TextField()


def test_parent_key_without_id_field():
    c = Company()
    c.name = 'testing parent key without id field'
    c.save()

    e1 = Employee(parent=c.key)
    e1.address = 'testing parent student key without field'
    e1.save()

    e2 = Employee.collection.get(e1.key)
    assert e1.id == e2.id
    assert e1.key == e2.key


def test_parent_key_with_value():
    c = Company()
    c.id = 'test_parent_key_with_value'
    c.name = 'testing parent key with value'
    c.save()

    e1 = Employee(parent=c.key)
    e1.id = 'student_test_parent_key_with_values'
    e1.address = 'testing parent student key with value'
    e1.save()

    e2 = Employee.collection.get(e1.key)
    assert e1.id == e2.id
    assert e1.key == e2.key


def test_parent_key_with_id_name():
    c = Company()
    c.id = 'test_parent_key_with_id_name'
    c.name = 'testing parent key with value'
    c.save()

    e1 = Employee(parent=c.key)
    e1.id = 'student_test_parent_key_with_id_name'
    e1.address = 'testing parent student key with value'
    e1.save()

    e2 = Employee.collection.get(e1.key)
    assert e1.id == e2.id
    assert e1.key == e2.key

    assert e1.id != 'test_parent_key_with_id_name'
    assert e2.id != 'test_parent_key_with_id_name'