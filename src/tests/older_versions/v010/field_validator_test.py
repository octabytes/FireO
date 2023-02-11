import pytest
from fireo.fields import TextField
from fireo.fields.errors import FieldValidationFailed, ValidatorNotCallable
from fireo.models import Model
from fireo.models.errors import ModelSerializingError


class Student(Model):
    name = TextField(validator="not_callable")


def test_non_callable_validator():
    s = Student()
    s.name = "Azeem"
    with pytest.raises(ModelSerializingError) as e:
        s.save()

    assert isinstance(e.value.original_error, ValidatorNotCallable)


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
    with pytest.raises(ModelSerializingError) as e:
        e2.save()

    assert isinstance(e.value.original_error, FieldValidationFailed)


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
    with pytest.raises(ModelSerializingError) as e:
        u2.save()

    assert isinstance(e.value.original_error, FieldValidationFailed)
    assert 'name_is_not_correct' in str(e.value)