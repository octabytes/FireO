from fireo.fields import TextField, NumberField, DateTime
from fireo.models import Model


class StartAfterPages(Model):
    name = TextField()
    order = NumberField()
    created_on = DateTime(auto=True)


# Sample data

StartAfterPages.collection.create(name='page1', order=1)
StartAfterPages.collection.create(name='page2', order=1)
StartAfterPages.collection.create(name='page3', order=2)
StartAfterPages.collection.create(name='page4', order=2)
StartAfterPages.collection.create(name='page5', order=3)
StartAfterPages.collection.create(name='page6', order=3)
StartAfterPages.collection.create(name='page7', order=4)
StartAfterPages.collection.create(name='page8', order=4)
StartAfterPages.collection.create(name='page9', order=5)
StartAfterPages.collection.create(name='page10', order=5)
StartAfterPages.collection.create(name='page11', order=6)


def test_start_after_with_key():
    pages = StartAfterPages.collection.order('created_on').fetch(3)

    last_doc_key = None

    for page in pages:
        last_doc_key = page.key

    assert last_doc_key is not None

    pages = StartAfterPages.collection.order('created_on').start_after(key=last_doc_key).fetch(3)

    for page in pages:
        assert page.key != last_doc_key
        assert page.name not in ['page1', 'page2', 'page3']


def test_start_after_with_fields():
    pages = StartAfterPages.collection.order('order').start_after(order=3).fetch(3)

    for page in pages:
        assert page.order not in [1,2]