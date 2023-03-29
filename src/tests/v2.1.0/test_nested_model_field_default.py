from fireo.fields import NestedModelField, TextField
from fireo.models import Model


class MyNestedModel(Model):
    field = TextField()


class MyModel(Model):
    my_nested = NestedModelField(
        MyNestedModel,
        default_factory=lambda: MyNestedModel(field="default value")
    )


def test_save_with_default():
    my_model = MyModel()
    my_model.save()

    assert my_model.my_nested.field == "default value"
