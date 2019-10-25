from fireo.fields import IDField, TextField, BooleanField, NumberField, ListField
from fireo.models import Model


class CityOrderAndLimit(Model):
    short_name = IDField()
    name = TextField()
    state = TextField()
    country = TextField()
    capital = BooleanField()
    population = NumberField()
    regions = ListField()

CityOrderAndLimit.collection.create(
short_name='SF', name='San Francisco', state='CA', country='USA',
capital=False, population=860000, regions=['west_coast', 'norcal']
)

CityOrderAndLimit.collection.create(
short_name='LA', name='Los Angeles', state='CA', country='USA',
capital=False, population=3900000, regions=['west_coast', 'socal']
)

CityOrderAndLimit.collection.create(
short_name='DC', name='Washington D.C.', state='CA', country='USA',
capital=True, population=680000, regions=['east_coast']
)

CityOrderAndLimit.collection.create(
short_name='TOK', state=None, name='Tokyo', country='Japan',
capital=True, population=9000000, regions=['kanto', 'honshu']
)

CityOrderAndLimit.collection.create(
short_name='BJ', name='Beijing', country='China',
capital=True, population=21500000, regions=['hebei']
)

name_list = ['Beijing', 'Los Angeles', 'San Francisco', 'Tokyo', 'Washington D.C.']

def test_limit_query():
    cities = CityOrderAndLimit.collection.limit(3).fetch()

    index = 0
    for c in cities:
        index = index + 1

    assert index == 3


def test_fetch_limit():
    cities = CityOrderAndLimit.collection.fetch(3)

    index = 0
    for c in cities:
        index = index + 1

    assert index == 3


def test_order_query():
    cities = CityOrderAndLimit.collection.order('name').fetch()

    for index, city in enumerate(cities):
        assert city.name == name_list[index]


def test_reverse_order_query():
    cities = CityOrderAndLimit.collection.order('-name').fetch()

    index = 4
    for c in cities:
        assert c.name == name_list[index]
        index = index - 1


def test_order_with_limit_query():
    cities = CityOrderAndLimit.collection.order('name').limit(3).fetch()

    index = 0
    for c in cities:
        assert c.name == name_list[index]
        index = index + 1

    assert index == 3