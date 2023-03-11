import pytest

import fireo
from fireo.fields import NumberField
from fireo.fields.errors import InvalidFieldType
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class MyModel(Model):
    my_int_field = NumberField(int_only=True)
    my_float_field = NumberField(float_only=True)


def test_increment_value():
    model = MyModel(
        my_int_field=fireo.Increment(1),
        my_float_field=fireo.Increment(2.0),
    )
    model.save()

    assert model.my_int_field == 1
    assert model.my_float_field == 2.0


def test_increment_using_float_instead_of_int_raises_error():
    model = MyModel(
        my_int_field=fireo.Increment(1.5),
    )

    with pytest.raises(ModelSerializingWrappedError) as error:
        model.save()

    assert isinstance(error.value.__cause__, InvalidFieldType)
    assert 'my_int_field' in str(error.value)


def test_increment_using_int_instead_of_float_raises_error():
    model = MyModel(
        my_float_field=fireo.Increment(1),
    )

    with pytest.raises(ModelSerializingWrappedError) as error:
        model.save()

    assert isinstance(error.value.__cause__, InvalidFieldType)
    assert 'my_float_field' in str(error.value)