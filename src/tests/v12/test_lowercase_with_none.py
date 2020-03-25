from fireo.fields import TextField
from fireo.models import Model


def test_lowercase_model_with_none_value():
    class LowercaseNone(Model):
        name = TextField()
        address = TextField()

        class Meta:
            to_lowercase = True


    ln = LowercaseNone()
    ln.name = 'name'
    ln.save()

    ln2 = LowercaseNone.collection.get(ln.key)

    assert ln2.name == 'name'
    assert ln2.address is None


def test_lowercase_field_with_none_value():
    class LowercaseNone(Model):
        name = TextField()
        address = TextField(to_lowercase=True)


    ln = LowercaseNone()
    ln.name = 'name'
    ln.save()

    ln2 = LowercaseNone.collection.get(ln.key)

    assert ln2.name == 'name'
    assert ln2.address is None