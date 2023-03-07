from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    text = TextField()
    unique = TextField()


def test_none_should_remove_limit():
    for i in range(10):
        MyModel(text=str(i), unique='test_none_should_remove_limit').save()

    query = MyModel.collection.filter(unique='test_none_should_remove_limit').limit(5)
    items = list(query.limit(None).fetch())

    assert len(items) == 10


def test_cursor_contains_limit():
    for i in range(10):
        MyModel(text=str(i)).save()

    query = MyModel.collection.filter().limit(3)
    query_iterator = query.fetch()
    cursor = query_iterator.cursor

    items = list(MyModel.collection.cursor(cursor).fetch())

    assert len(items) == 3


def test_cursor_contains_limit_overwritten_in_fetch():
    for i in range(10):
        MyModel(text=str(i)).save()

    query = MyModel.collection.filter().limit(3)
    query_iterator = query.fetch(4)
    cursor = query_iterator.cursor

    items = list(MyModel.collection.cursor(cursor).fetch())

    assert len(items) == 4
