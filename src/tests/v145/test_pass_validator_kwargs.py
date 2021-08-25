from fireo import fields
from fireo.models import Model

def validator_func_with_kwargs(a, **kwargs):
    if kwargs.get("some_key"):
        return True

    return False 


class Test(Model): 
    name = fields.TextField(required=True, validator=validator_func_with_kwargs, validator_kwargs={"some_key": "some_val"})

    class Meta:
        ignore_none_field = False


def test_pass_validator_kwargs():
    test = Test()
    test.name = "test"
    test.save()


