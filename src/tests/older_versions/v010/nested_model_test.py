from fireo.fields import TextField, NestedModel
from fireo.models import Model


class User(Model):
    name = TextField()


class Student(Model):
    address = TextField()
    user = NestedModel(User)


def test_save_nested():
    u = User(name='Nested_Model')

    s = Student(address="Student_address")
    s.user = u
    s.save()

    s2 = Student.collection.get(s.key)
    assert s2.address == 'Student_address'
    assert s2.user.name == 'Nested_Model'


def test_update_nested():
    u = User(name='Nested_Model')

    s = Student(address="Student_address")
    s.user = u
    s.save()

    s2 = Student.collection.get(s.key)
    s2.address = 'Updated_address'
    s2.update()

    s3 = Student.collection.get(s.key)
    assert s3.address == 'Updated_address'
    assert s3.user.name == 'Nested_Model'