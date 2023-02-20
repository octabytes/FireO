from fireo.fields import ListField
from fireo.models import Model


class MyModel(Model):
    field = ListField(default=[])


def test_copy_default_mutable_values():
    model1 = MyModel()
    model1.save()
    model2 = MyModel()
    model2.save()

    assert model1.field is not model2.field
