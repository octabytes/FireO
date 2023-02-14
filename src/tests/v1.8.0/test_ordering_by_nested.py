from fireo.fields import MapField, NestedModelField
from fireo.models import Model


class Nested(Model):
    b = MapField(column_name='bb')


class TestModel(Model):
    a = NestedModelField(Nested, column_name='aa')


def test_order_by_nested():
    TestModel.from_dict({'a': {'b': {'c': {'d': 1}}}}).save()
    TestModel.from_dict({'a': {'b': {'c': {'d': 2}}}}).save()
    TestModel.from_dict({'a': {'b': {'c': {'d': 3}}}}).save()

    assert [m.a.b['c']['d'] for m in TestModel.collection.order('a.b.c.d').fetch()] == [1, 2, 3]
    assert [m.a.b['c']['d'] for m in TestModel.collection.order('-a.b.c.d').fetch()] == [3, 2, 1]
