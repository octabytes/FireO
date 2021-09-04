from fireo.fields import NumberField, DateTime
from fireo.models import Model


class OffsetModel(Model):
    num = NumberField()
    created_on = DateTime(auto=True)


for n in range(10):
    OffsetModel.collection.create(num=n)


def test_simple_offset():
    docs = OffsetModel.collection.order('created_on').offset(3).fetch(3)

    for doc in docs:
        assert doc.num in (3, 4, 5)
