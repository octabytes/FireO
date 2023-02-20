from fireo.fields import ListField, NestedModelField, TextField
from fireo.models import Model


class MyNestedModel(Model):
    field1 = TextField()
    field2 = TextField()
    field3 = TextField()


class MyModel(Model):
    field1 = TextField()
    field2 = TextField()
    field3 = TextField()
    nested = NestedModelField(MyNestedModel)
    nested_list = ListField(NestedModelField(MyNestedModel))


def test_merge_with_dict_works_with_nested():
    model = MyModel()
    model.field1 = "value1"
    model.field2 = "value2"
    model.field3 = "value3"
    model.nested.field1 = "nested_value1"
    model.nested.field2 = "nested_value2"
    model.nested.field3 = "nested_value3"

    model.merge_with_dict({
        "field1": None,
        "field2": "changed_value2",
        "nested": {
            "field1": None,
            "field2": "changed_nested_value2",
        }
    })

    assert model.field1 is None
    assert model.field2 == "changed_value2"
    assert model.field3 == "value3"
    assert model.nested.field1 is None
    assert model.nested.field2 == "changed_nested_value2"
    assert model.nested.field3 == "nested_value3"


def test_merge_with_dict_replaces_list_values():
    model = MyModel()
    model.nested_list = [
        MyNestedModel(field1="value1", field2="value2", field3="value3"),
        MyNestedModel(field1="value4", field2="value5", field3="value6"),
    ]
    model.merge_with_dict({
        "nested_list": [
            {"field1": "changed_value1", "field2": "changed_value2"},
        ]
    })

    assert len(model.nested_list) == 1
    assert model.nested_list[0].field1 == "changed_value1"
    assert model.nested_list[0].field2 == "changed_value2"
    assert model.nested_list[0].field3 is None
