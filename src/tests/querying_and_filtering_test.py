from fireo.fields import IDField, TextField, BooleanField, NumberField, ListField
from fireo.models import Model


class CityQueryAndFiltering(Model):
    short_name = IDField()
    name = TextField()
    state = TextField()
    country = TextField()
    capital = BooleanField()
    population = NumberField()
    regions = ListField()

CityQueryAndFiltering.collection.create(
short_name='SF', name='San Francisco', state='CA', country='USA',
capital=False, population=860000, regions=['west_coast', 'norcal']
)

CityQueryAndFiltering.collection.create(
short_name='LA', name='Los Angeles', state='CA', country='USA',
capital=False, population=3900000, regions=['west_coast', 'socal']
)

CityQueryAndFiltering.collection.create(
short_name='DC', name='Washington D.C.', state='CA', country='USA',
capital=True, population=680000, regions=['east_coast']
)

CityQueryAndFiltering.collection.create(
short_name='TOK', state=None, name='Tokyo', country='Japan',
capital=True, population=9000000, regions=['kanto', 'honshu']
)

CityQueryAndFiltering.collection.create(
short_name='BJ', name='Beijing', country='China',
capital=True, population=21500000, regions=['hebei']
)


def test_simple_query():
    cities = CityQueryAndFiltering.collection.filter('state', '==', 'CA').fetch()

    for c in cities:
        assert c.state == 'CA'


def test_simple_query_bool():
    cities = CityQueryAndFiltering.collection.filter('capital', '==', True).fetch()

    for c in cities:
        assert c.capital == True


def test_smiple_query_first_result():
    city = CityQueryAndFiltering.collection.filter('state', '==', 'CA').get()

    assert city.state == 'CA'


def test_query_list_membership():
    cities = CityQueryAndFiltering.collection.filter('regions', 'array_contains', 'west_coast').fetch()

    for c in cities:
        assert 'west_coast' in c.regions


def test_compund_query():
    cities = CityQueryAndFiltering.collection.filter('state', '==', 'CO').filter('name', '==', 'Denver').fetch()

    for c in cities:
        assert c.state == 'CO'
        assert c.name == 'Denver'
