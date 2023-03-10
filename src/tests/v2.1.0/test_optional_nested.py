from fireo.fields import NestedModelField, TextField
from fireo.models import Model


class MyNested(Model):
    my_required_field = TextField(required=True)


class MyModel(Model):
    some_field = TextField()
    my_nested = NestedModelField(MyNested)


def test_can_create_model_without_optional_nested_model():
    my_model = MyModel()
    my_model.some_field = "some value"

    assert my_model.my_nested is None
    my_model.save()
