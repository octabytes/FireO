from fireo.fields import TextField, NumberField, DateTime
from fireo.models import Model


class StartEndAfterAt(Model):
    name = TextField()
    order = NumberField()
    created_on = DateTime(auto=True)


# Sample data

StartEndAfterAt.collection.create(name='page1', order=1)
StartEndAfterAt.collection.create(name='page2', order=1)
StartEndAfterAt.collection.create(name='page3', order=2)
StartEndAfterAt.collection.create(name='page4', order=2)
StartEndAfterAt.collection.create(name='page5', order=3)
StartEndAfterAt.collection.create(name='page6', order=3)
StartEndAfterAt.collection.create(name='page7', order=4)
StartEndAfterAt.collection.create(name='page8', order=4)
StartEndAfterAt.collection.create(name='page9', order=5)
StartEndAfterAt.collection.create(name='page10', order=5)
StartEndAfterAt.collection.create(name='page11', order=6)


def test_start_after_with_key():
    pages = StartEndAfterAt.collection.order('created_on').fetch(3)

    last_doc_key = None

    for page in pages:
        last_doc_key = page.key

    assert last_doc_key is not None

    pages = StartEndAfterAt.collection.order('created_on').start_after(key=last_doc_key).fetch(3)

    for page in pages:
        assert page.key != last_doc_key
        assert page.name not in ['page1', 'page2', 'page3']


def test_start_after_with_fields():
    pages = StartEndAfterAt.collection.order('order').start_after(order=3).fetch(3)

    for page in pages:
        assert page.order not in [1,2]


def test_start_at_with_key():
    pages = StartEndAfterAt.collection.order('created_on').fetch(3)

    last_doc_key = None

    for page in pages:
        last_doc_key = page.key

    assert last_doc_key is not None

    pages = StartEndAfterAt.collection.order('created_on').start_at(key=last_doc_key).fetch(3)

    for page in pages:
        assert page.name in ['page3', 'page4', 'page5']


def test_start_at_with_fields():
    pages = StartEndAfterAt.collection.order('order').start_at(order=3).fetch(3)

    for page in pages:
        assert page.order != 1


def test_end_before_with_key():
    pages = StartEndAfterAt.collection.order('created_on').fetch(3)

    last_doc_key = None

    for page in pages:
        last_doc_key = page.key

    assert last_doc_key is not None

    pages = StartEndAfterAt.collection.order('created_on').end_before(key=last_doc_key).fetch(3)

    for page in pages:
        assert page.key != last_doc_key
        assert page.name in ['page1', 'page2']


def test_end_before_with_fields():
    pages = StartEndAfterAt.collection.order('order').end_before(order=3).fetch(3)

    for page in pages:
        assert page.order in [1,2]


def test_end_at_with_key():
    pages = StartEndAfterAt.collection.order('created_on').fetch(3)

    last_doc_key = None

    for page in pages:
        last_doc_key = page.key

    assert last_doc_key is not None

    pages = StartEndAfterAt.collection.order('created_on').end_at(key=last_doc_key).fetch(3)

    for page in pages:
        assert page.name in ['page1', 'page2', 'page3']


def test_end_at_with_fields():
    pages = StartEndAfterAt.collection.order('order').end_at(order=3).fetch(3)

    for page in pages:
        assert page.order in [1,2,3]