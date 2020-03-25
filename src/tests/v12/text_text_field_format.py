from fireo.fields import TextField
from fireo.models import Model


def test_format_with_none_value():
    class TextFieldFormatNone(Model):
        name = TextField()
        address = TextField(format='upper')

    t = TextFieldFormatNone()
    t.name = 'name'
    t.save()

    tf = TextFieldFormatNone.collection.get(t.key)\

    assert tf.name == 'name'
    assert tf.address is None