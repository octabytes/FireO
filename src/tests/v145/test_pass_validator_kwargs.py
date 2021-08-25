import pytest

from fireo import fields
from fireo.models import Model
from fireo.fields.errors import FieldValidationFailed


def validator_func_check_kwargs(a, **kwargs):
    if kwargs.get("some_key"):
        return True 

    return False


def validator_func(a):
    return True


def validator_func_optional_kwargs(a, **kwargs):
    return True 


class TestA(Model): 
    name = fields.TextField(required=True, validator=validator_func_check_kwargs, validator_kwargs={"some_key": "some_val"})


class TestB(Model):
    name = fields.TextField(required=True, validator=validator_func, validator_kwargs={"some_key": "some_val"})


class TestC(Model): 
    name = fields.TextField(required=True, validator=validator_func_optional_kwargs)


def test_pass_validator_kwargs():
    test = TestA()
    test.name = "test"
    test.save()


def test_validator_func_without_kwargs_raises_exception():
    with pytest.raises(FieldValidationFailed):
        test = TestB()
        test.name = "test"
        test.save()


def test_no_kwargs_passed_to_validator_func_with_kwargs():
    test = TestC()
    test.name = "test"
    test.save()
