from fireo.fields import TextField, MapField, NestedModel
from fireo.models import Model


class User(Model):
    name = TextField()


class Student(Model):
    address = TextField()
    user = NestedModel(User)
    classes = MapField()


def test_query_nested_and_map():
    u = User(name='Nested_Model')

    s = Student(address="Student_address")
    s.user = u
    s.classes = {"physics": 101,
                 "history": 201,
                 "physics": 404}
    s.save()
    value = Student.collection.filter("user.name", "==", "Nested_Model").get()
    assert value.user.name == "Nested_Model"
    value = Student.collection.filter("classes.physics", ">", 400).get()
    assert value.user.name == "Nested_Model"
