from fireo.fields import TextField, NumberField
from fireo.models import Model


class CursorPages(Model):
    name = TextField()
    order = NumberField()


# Sample data

CursorPages.collection.create(name='page1', order=1)
CursorPages.collection.create(name='page2', order=1)
CursorPages.collection.create(name='page3', order=2)
CursorPages.collection.create(name='page4', order=2)
CursorPages.collection.create(name='page5', order=3)
CursorPages.collection.create(name='page6', order=3)
CursorPages.collection.create(name='page7', order=4)
CursorPages.collection.create(name='page8', order=4)
CursorPages.collection.create(name='page9', order=5)
CursorPages.collection.create(name='page10', order=5)
CursorPages.collection.create(name='page11', order=6)


def test_simple_cursor():
    pages = CursorPages.collection.order('order').fetch(3)

    page_list1 = ['page1', 'page2', 'page3', 'page4']

    for page in pages:
        print(page.order, page.name)
        assert page.name in page_list1

    c = pages.cursor

    pages = CursorPages.collection.cursor(c).fetch(3)

    for page in pages:
        assert page.name in ['page3', 'page4', 'page5', 'page6']


def test_cursor_with_offset():
    pages = CursorPages.collection.order('order').fetch(3)
    c = pages.cursor

    pages = CursorPages.collection.cursor(c).fetch(3)

    for page in pages:
        assert page.name != 'page1'


def test_cursor_with_filter():
    pages = CursorPages.collection.filter('order', '>=', 2).order('order').fetch(3)

    for page in pages:
        assert page.name != 'page1'

    c = pages.cursor

    pages = CursorPages.collection.cursor(c).fetch(3)

    for page in pages:
        assert page.name != 'page1'