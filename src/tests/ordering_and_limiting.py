from fireo.fields import IDField, TextField, BooleanField, NumberField, ListField
from fireo.models import Model


class City(Model):
    short_name = IDField()
    name = TextField()
    state = TextField()
    country = TextField()
    capital = BooleanField()
    population = NumberField()
    regions = ListField()

City.collection.create(
short_name='SF', name='San Francisco', state='CA', country='USA',
capital=False, population=860000, regions=['west_coast', 'norcal']
)

City.collection.create(
short_name='LA', name='Los Angeles', state='CA', country='USA',
capital=False, population=3900000, regions=['west_coast', 'socal']
)

City.collection.create(
short_name='DC', name='Washington D.C.', state='CA', country='USA',
capital=True, population=680000, regions=['east_coast']
)

City.collection.create(
short_name='TOK', state=None, name='Tokyo', country='Japan',
capital=True, population=9000000, regions=['kanto', 'honshu']
)

City.collection.create(
short_name='BJ', name='Beijing', country='China',
capital=True, population=21500000, regions=['hebei']
)


def test_limit_query():
    cities = City.collection.order('name').limit(3).fetch()

    index = 0
    for c in cities:
        index = index + 1

    assert index == 3


def test_fetch_limit():
    cities = City.collection.order('name').fetch(3)

    index = 0
    for c in cities:
        index = index + 1

    assert index == 3

