from fireo.fields import TextField, NumberField
from fireo.models import Model


class User(Model):
    name = TextField()
    age = NumberField()


def test_query_limit():
    u1 = User(name="Azeem", age=25)
    u1.save()
    u2 = User(name="Arfan", age=26)
    u2.save()
    u3 = User(name="Haider", age=27)
    u3.save()

    docs = User.collection.fetch(3)
    index = 0
    for doc in docs:
        index = index + 1

    assert index == 3


def test_filter_query():
    docs = User.collection.filter('age', '>', '24').fetch()

    for doc in docs:
        assert doc.age > 24


def test_query_get():
    u = User.collection.filter('name', '==', 'Azeem').get()

    assert u.name == 'Azeem'


class User1(Model):
    name = TextField()


class Student(Model):
    age = NumberField()


def test_parent_filter():
    u = User1(name="Arfan")
    u.save()
    s = Student(parent=u.key)
    s.age = 26
    s.save()

    docs = Student.collection.parent(u.key).filter('age', '==', 26).fetch()

    for doc in docs:
        assert doc.age == 26


def test_delete_document():
    u = User(name="Arfan", age=27)
    u.save()

    User.collection.delete(u.key)

    u2 = User.collection.get(u.key)

    assert u2 is None


def test_delete_filter_document():
    User.collection.filter('age', '==', 27).delete()

    docs = User.collection.filter('age', '==', 27).fetch()
    doc = next(docs, None)

    assert doc is None


class Uni(Model):
    name = TextField()


def test_query_fetch_doc():
    Uni.collection.create(name="First Uni")
    Uni.collection.create(name="Second Uni")
    Uni.collection.create(name="Third Uni")

    name_list = ['First Uni', 'Second Uni', 'Third Uni', 'Parent Uni']

    uni_list = Uni.collection.fetch()

    for u in uni_list:
        assert u.name in name_list


class Teacher(Model):
    age = NumberField()


def test_query_fetch_parent_doc():
    u = Uni.collection.create(name="Parent Uni")

    Teacher.collection.create(parent=u.key, age=25)
    Teacher.collection.create(parent=u.key, age=26)
    Teacher.collection.create(parent=u.key, age=27)

    t_age = [25, 26, 27]

    teacher_list = Teacher.collection.parent(u.key).fetch()

    for t in teacher_list:
        assert t.age in t_age

