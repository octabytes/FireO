import random

from fireo.fields import TextField, DateTime, NumberField
from fireo.models import Model


class NextFetchModel(Model):
    name = TextField()
    age = NumberField()
    order_num = NumberField()
    created_on = DateTime(auto=True)


# Sample Data for testing
age_list = [20, 18, 23, 17, 25, 26, 27]

for n in range(20):
    NextFetchModel.collection.create(name='page' + str(n), age=random.choice(age_list), order_num=n)


def test_simple_next_fetch():
    pages = NextFetchModel.collection.order('order_num').fetch(5)

    page_list = ['page0', 'page1', 'page2', 'page3', 'page4']

    for page in pages:
        assert page.name in page_list

    pages.next_fetch()

    page_list2 = ['page5', 'page6', 'page7', 'page8', 'page9']

    for page in pages:
        assert page.name in page_list2


def test_new_limit_with_next_fetch():
    pages = NextFetchModel.collection.order('order_num').fetch(5)

    page_list = ['page0', 'page1', 'page2', 'page3', 'page4']

    counter = 0
    for page in pages:
        assert page.name in page_list
        counter += 1

    assert counter == 5

    pages.next_fetch(3)

    page_list2 = ['page5', 'page6', 'page7']

    counter2 = 0
    for page in pages:
        assert page.name in page_list2
        counter2 += 1

    assert counter2 == 3

    pages.next_fetch()

    page_list3 = ['page8', 'page9', 'page10', 'page11', 'page12']

    counter3 = 0
    for page in pages:
        assert page.name in page_list3
        counter3 += 1

    assert counter3 == 5


def test_offset_in_next_fetch():
    pages = NextFetchModel.collection.order('order_num').fetch(3)
    page_list = ['page1', 'page2', 'page3', 'page4', 'page5']

    p = next(pages).name
    assert p == 'page0'

    pages.next_fetch()

    index = 0
    for page in pages:
        assert page.name in page_list
        index += 1

    assert index == 5


def test_fetch_without_next():
    pages = NextFetchModel.collection.order('order_num').fetch(3)
    page_list = ['page0', 'page1', 'page2', 'page3', 'page4', 'page5']

    pages.next_fetch()

    index = 0
    for page in pages:
        assert page.name in page_list
        index += 1

    assert index == 6


def test_delete_all_next_fetch():
    NextFetchModel.collection.delete()