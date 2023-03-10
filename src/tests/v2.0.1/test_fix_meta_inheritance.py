from fireo.fields import TextField
from fireo.models import Model


class BaseMeta:
    missing_field = 'ignore'


class MyModel(Model):
    class Meta(BaseMeta):
        to_lowercase = True

    some_field = TextField()


def test_mete_inheritance():
    assert MyModel._meta.missing_field == 'ignore'
    assert MyModel._meta.to_lowercase is True
