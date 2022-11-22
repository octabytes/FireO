import pytest
from fireo.fields import TextField
from fireo.fields.errors import FieldValidationFailed, ValidatorNotCallable
from fireo.models import Model


class Student(Model):
    name = TextField(validator="not_callable")


def test_non_callable_validator():
    s = Student()
    s.name = "Azeem"
    with pytest.raises(ValidatorNotCallable):
        s.save()


def check_emp_name(value):
    if value == 'Azeem':
        return True
    else:
        return False


class Employee(Model):
    name = TextField(validator=check_emp_name)


def test_field_validator():
    e = Employee()
    e.name = 'Azeem'
    e.save()

    e2 = Employee()
    e2.name = 'Arfan'
    with pytest.raises(FieldValidationFailed):
        e2.save()


def check_emp_name_with_err(value):
    if value == 'Azeem':
        return True
    else:
        return (False, 'name_is_not_correct')


class User(Model):
    name = TextField(validator=check_emp_name_with_err)


def test_validator_with_custom_err():
    u = User()
    u.name = 'Azeem'
    u.save()

    u2 = User()
    u2.name = 'Arfan'
    with pytest.raises(FieldValidationFailed) as e:
        u2.save()

    assert 'name_is_not_correct' in str(e.value)