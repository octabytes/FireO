import pytest

from fireo.fields import NumberField
from fireo.fields.errors import NumberRangeError
from fireo.models import Model


class RangeNumberField(Model):
    number = NumberField(range=(1, 5))


def test_range_start_stop_number():
    r1 = RangeNumberField.collection.create(number=1)
    r2 = RangeNumberField.collection.get(r1.key)
    assert r2.number == 1

    r1 = RangeNumberField.collection.create(number=5)
    r2 = RangeNumberField.collection.get(r1.key)
    assert r2.number == 5

    r1 = RangeNumberField.collection.create(number=3)
    r2 = RangeNumberField.collection.get(r1.key)
    assert r2.number == 3

    with pytest.raises(NumberRangeError):
        RangeNumberField.collection.create(number=0)

    with pytest.raises(NumberRangeError):
        RangeNumberField.collection.create(number=6)


class RangeNumberField1(Model):
    number = NumberField(range=(3))


def test_range_start_only_number():
    r1 = RangeNumberField1.collection.create(number=3)
    r2 = RangeNumberField1.collection.get(r1.key)
    assert r2.number == 3

    r1 = RangeNumberField1.collection.create(number=4)
    r2 = RangeNumberField1.collection.get(r1.key)
    assert r2.number == 4

    with pytest.raises(NumberRangeError):
        RangeNumberField1.collection.create(number=2)