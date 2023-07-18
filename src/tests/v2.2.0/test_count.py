from fireo.fields import NumberField, TextField
from fireo.models import Model


class MyCountModel(Model):
    field_1 = NumberField()
    field_2 = TextField()


def test_count():
    MyCountModel.collection.create(field_1=1, field_2="a")
    MyCountModel.collection.create(field_1=2, field_2="b")
    MyCountModel.collection.create(field_1=3, field_2="c")

    assert MyCountModel.collection.filter('field_1', '>=', 2).count() == 2
