from fireo.fields import TextField
from fireo.models import Model


def test_lowercase_single_field():
    class LowercaseModel(Model):
        name = TextField()
        address = TextField(to_lowercase=True)

    lc = LowercaseModel()
    lc.name = 'Name'
    lc.address = 'ADDRESS'
    lc.save()

    lc2 = LowercaseModel.collection.get(lc.key)

    assert lc2.name == 'Name'
    assert lc2.address == 'address'


def test_text_lowercase_single_field():
    class LowercaseModel(Model):
        name = TextField()
        address = TextField(to_lowercase=False)

    lc = LowercaseModel()
    lc.name = 'Name'
    lc.address = 'ADDRESS'
    lc.save()

    lc2 = LowercaseModel.collection.get(lc.key)

    assert lc2.name == 'Name'
    assert lc2.address == 'ADDRESS'
