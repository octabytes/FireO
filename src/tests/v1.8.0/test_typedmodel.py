import sys
from typing import List, Optional, Union

from google.cloud import firestore

from fireo.fields import (
    BooleanField,
    GeoPoint,
    ListField,
    MapField,
    NestedModelField,
    NumberField,
    TextField,
)
from fireo.typedmodels import TypedModel


class Deep1Model(TypedModel):
    nested_int: int


class RootModel(TypedModel):
    int_: int
    float_: float
    int_or_float: Union[int, float]
    optional_int_or_float: Optional[Union[int, float]]
    none_int_or_float: Union[None, int, float]
    str_: str
    bool_: bool
    list_: list
    dict_: dict
    geo_point: firestore.GeoPoint
    optional_int: Optional[int]

    list_of_int: List[int]
    list_of_int_or_none: List[Optional[int]]
    none_or_list_of_int: Union[None, List[int]]

    int_with_default: int = 1
    optional_int_with_default: Optional[int] = 1

    override_type: Optional[str] = NumberField(required=True)

    nested: Deep1Model
    list_of_nested: List[Deep1Model]


def test_generated_fields():
    fields = RootModel._meta.field_list
    assert fields['int_'].__class__ is NumberField
    assert fields['int_'].raw_attributes == {'int_only': True, 'required': True}

    assert fields['float_'].__class__ is NumberField
    assert fields['float_'].raw_attributes == {'float_only': True, 'required': True}

    assert fields['int_or_float'].__class__ is NumberField
    assert fields['int_or_float'].raw_attributes == {'required': True}

    assert fields['optional_int_or_float'].__class__ is NumberField
    assert fields['optional_int_or_float'].raw_attributes == {'required': False}

    assert fields['none_int_or_float'].__class__ is NumberField
    assert fields['none_int_or_float'].raw_attributes == {'required': False}

    assert fields['str_'].__class__ is TextField
    assert fields['str_'].raw_attributes == {'required': True}

    assert fields['bool_'].__class__ is BooleanField
    assert fields['bool_'].raw_attributes == {'required': True}

    assert fields['list_'].__class__ is ListField
    assert fields['list_'].raw_attributes == {'required': True, 'nested_field': None}

    assert fields['dict_'].__class__ is MapField
    assert fields['dict_'].raw_attributes == {'required': True}

    assert fields['geo_point'].raw_attributes == {'required': True}
    assert fields['geo_point'].__class__ is GeoPoint

    assert fields['optional_int'].__class__ is NumberField
    assert fields['optional_int'].raw_attributes == {'int_only': True, 'required': False}

    assert fields['list_of_int'].__class__ is ListField
    assert fields['list_of_int'].raw_attributes['required'] is True
    assert fields['list_of_int'].raw_attributes['nested_field'].__class__ is NumberField
    assert fields['list_of_int'].raw_attributes['nested_field'].raw_attributes == {
        'int_only': True,
        'required': True
    }

    assert fields['list_of_int_or_none'].__class__ is ListField
    assert fields['list_of_int_or_none'].raw_attributes['required'] is True
    assert fields['list_of_int_or_none'].raw_attributes['nested_field'].__class__ is NumberField
    assert fields['list_of_int_or_none'].raw_attributes['nested_field'].raw_attributes == {
        'int_only': True, 'required': False
    }

    assert fields['none_or_list_of_int'].__class__ is ListField
    assert fields['none_or_list_of_int'].raw_attributes['required'] is False
    assert fields['none_or_list_of_int'].raw_attributes['nested_field'].__class__ is NumberField
    assert fields['none_or_list_of_int'].raw_attributes['nested_field'].raw_attributes == {
        'int_only': True, 'required': True
    }

    assert fields['int_with_default'].__class__ is NumberField
    assert fields['int_with_default'].raw_attributes == {'int_only': True, 'required': True, 'default': 1}

    assert fields['optional_int_with_default'].__class__ is NumberField
    assert fields['optional_int_with_default'].raw_attributes == {'int_only': True, 'required': False, 'default': 1}

    assert fields['override_type'].__class__ is NumberField
    assert fields['override_type'].raw_attributes == {'required': True}

    assert fields['nested'].__class__ is NestedModelField
    assert fields['nested'].raw_attributes == {'required': True}
    assert fields['nested'].nested_model == Deep1Model
    assert Deep1Model._meta.field_list['nested_int'].raw_attributes == {'int_only': True, 'required': True}

    assert fields['list_of_nested'].__class__ is ListField
    assert fields['list_of_nested'].raw_attributes['required'] is True
    assert fields['list_of_nested'].raw_attributes['nested_field'].__class__ is NestedModelField
    assert fields['list_of_nested'].raw_attributes['nested_field'].raw_attributes == {'required': True}
    assert fields['list_of_nested'].raw_attributes['nested_field'].nested_model == Deep1Model


if sys.version_info >= (3, 10):
    class Py310RootModel(TypedModel):
        int_or_float: int | float
        optional_int_or_float: int | float | None
        optional_int: int | None
        list_of_int: list[int]
        list_of_int_or_none: list[int | None]
        none_or_list_of_int: None | list[int]
        optional_int_with_default: int | None = 1
        list_of_nested: list[Deep1Model]
        override_type: str | None = NumberField(required=True)

    def test_py310_generated_fields():
        fields = Py310RootModel._meta.field_list

        assert fields['int_or_float'].__class__ is NumberField
        assert fields['int_or_float'].raw_attributes == {'required': True}

        assert fields['optional_int_or_float'].__class__ is NumberField
        assert fields['optional_int_or_float'].raw_attributes == {'required': False}

        assert fields['optional_int'].__class__ is NumberField
        assert fields['optional_int'].raw_attributes == {'int_only': True, 'required': False}

        assert fields['list_of_int'].__class__ is ListField
        assert fields['list_of_int'].raw_attributes['required'] is True
        assert fields['list_of_int'].raw_attributes['nested_field'].__class__ is NumberField
        assert fields['list_of_int'].raw_attributes['nested_field'].raw_attributes == {
            'int_only': True,
            'required': True
        }

        assert fields['list_of_int_or_none'].__class__ is ListField
        assert fields['list_of_int_or_none'].raw_attributes['required'] is True
        assert fields['list_of_int_or_none'].raw_attributes['nested_field'].__class__ is NumberField
        assert fields['list_of_int_or_none'].raw_attributes['nested_field'].raw_attributes == {
            'int_only': True, 'required': False
        }

        assert fields['none_or_list_of_int'].__class__ is ListField
        assert fields['none_or_list_of_int'].raw_attributes['required'] is False
        assert fields['none_or_list_of_int'].raw_attributes['nested_field'].__class__ is NumberField
        assert fields['none_or_list_of_int'].raw_attributes['nested_field'].raw_attributes == {
            'int_only': True, 'required': True
        }

        assert fields['optional_int_with_default'].__class__ is NumberField
        assert fields['optional_int_with_default'].raw_attributes == {'int_only': True, 'required': False, 'default': 1}

        assert fields['list_of_nested'].__class__ is ListField
        assert fields['list_of_nested'].raw_attributes['required'] is True
        assert fields['list_of_nested'].raw_attributes['nested_field'].__class__ is NestedModelField
        assert fields['list_of_nested'].raw_attributes['nested_field'].raw_attributes == {'required': True}
        assert fields['list_of_nested'].raw_attributes['nested_field'].nested_model == Deep1Model

