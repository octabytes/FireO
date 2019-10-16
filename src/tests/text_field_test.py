from fireo.fields import TextField
from fireo.models import Model


class User(Model):
    name = TextField(max_length=3)


def test_text_max():
    u = User()
    u.name = "123456"
    u.save()

    u2 = User.collection.get(u.key)
    assert u2.name == "123"