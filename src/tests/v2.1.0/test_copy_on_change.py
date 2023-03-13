from copy import deepcopy

import fireo
from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    first = TextField()
    second = TextField()


def test_copy_filter_query_on_change():
    MyModel(first='test', second='test').save()
    MyModel(first='test2', second='test2').save()
    MyModel(first='test', second='test3').save()

    base_query = MyModel.collection.filter(first='test').order('second')
    kwargs = deepcopy(base_query._deconstruct())
    result = list(base_query.fetch())
    keys = [r.key for r in result]

    assert len(result) == 2
    assert result[0].first == 'test'
    assert result[0].second == 'test'
    assert result[1].first == 'test'
    assert result[1].second == 'test3'
    assert base_query.filter(second='test2') is not base_query
    assert base_query.transaction('fake') is not base_query
    assert base_query.batch(fireo.batch()) is not base_query
    assert base_query.limit(1) is not base_query
    assert base_query.offset(1) is not base_query
    assert base_query.start_after(first='fake') is not base_query
    assert base_query.start_at(first='fake') is not base_query
    assert base_query.end_before(first='fake') is not base_query
    assert base_query.end_at(first='fake') is not base_query
    assert base_query.order('first') is not base_query
    assert base_query.fetch(1)
    assert base_query.get()

    assert kwargs == base_query._deconstruct()
    assert [e.key for e in base_query.fetch()] == keys


def test_copy_manager_on_change():
    manager = MyModel.collection

    assert manager is not manager.parent('fake')
    assert manager._deconstruct()['parent_key'] != 'fake'

