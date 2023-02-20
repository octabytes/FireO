from fireo.fields import TextField
from fireo.models import Model


def test_call_default_factory_if_no_value():
    class MyModel(Model):
        field = TextField(default_factory=lambda: 'default factory')

    model = MyModel()
    model.save()
    assert model.field == 'default factory'


def test_default_factory_is_not_called_if_default_exists():
    class MyModel(Model):
        field = TextField(
            default_factory=lambda: 'default value',
            default='default value',
        )

    model = MyModel()
    model.save()
    assert model.field == 'default value'
