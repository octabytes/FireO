import pytest
from fireo.fields import Field
from fireo.fields.errors import AttributeMethodNotDefined
from fireo.models import Model


class Employee(Field):
    allowed_attributes = ['some_attr']


def test_extend_field_attr_method_not_defined():
    with pytest.raises(AttributeMethodNotDefined):
        class User8(Model):
            name = Employee(some_attr="value")

        u = User8.collection.create(name="Emp_name")


class CustomField(Field):
    allowed_attributes = ['change_value']

    def attr_change_value(self, attr_val, field_val):
        return field_val + attr_val


class User(Model):
    name = CustomField()


def test_custom_field_creation():
    u = User.collection.create(name="custom_field")
    u2 = User.collection.get(u.key)

    assert u2.name == 'custom_field'


class Student(Model):
    name = CustomField(change_value="change_me")


def test_custom_field_with_attr():
    s = Student.collection.create(name="custom_field")
    s2 = Student.collection.get(s.key)

    assert s2.name == 'custom_field' + 'change_me'
