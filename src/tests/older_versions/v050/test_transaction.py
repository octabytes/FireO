import pytest
from google.cloud.firestore_v1 import ReadAfterWriteError

import fireo
from fireo.fields import TextField, NumberField, IDField
from fireo.models import Model


class TransCity(Model):
    id = IDField()
    state = TextField()
    population = NumberField()


# sample data
t = TransCity.collection.create(id='AB', state='AB', population=100)
TransCity.collection.create(id='CD', state='CD', population=400)
TransCity.collection.create(id='EF', state='EF', population=500)
TransCity.collection.create(id='GH', state='GH', population=300)

def test_simple_transaction():
    @fireo.transactional
    def update_population(trans):
        city = TransCity.collection.get('trans_city/AB', trans)
        city.population = city.population + 1
        city.update(transaction=trans)

    transaction = fireo.transaction()
    update_population(transaction)

    city = TransCity.collection.get('trans_city/AB')

    assert city.population == 101


def test_filter_get_transaction():
    @fireo.transactional
    def update_population(trans):
        city = TransCity.collection.filter('state', '==', 'CD').transaction(trans).get()
        city.population = city.population + 1
        city.update(transaction=trans)

    transaction = fireo.transaction()
    update_population(transaction)

    city = TransCity.collection.get('trans_city/CD')

    assert city.population == 401


def test_filter_fetch_transaction():
    @fireo.transactional
    def update_population(trans):
        cities = TransCity.collection.filter('state', '==', 'EF').transaction(trans).fetch()
        city = next(cities)
        city.population = city.population + 1
        city.update(transaction=trans)

    transaction = fireo.transaction()
    update_population(transaction)

    city = TransCity.collection.get('trans_city/EF')

    assert city.population == 501


def test_error_read_after_write_transaction():
    @fireo.transactional
    def update_population(trans):
        TransCity.collection.create(transaction=trans, state='IJ', population=200)
        city = TransCity.collection.get('trans_city/AB', trans)
        city.population = city.population + 1
        city.update(transaction=trans)

    transaction = fireo.transaction()

    with pytest.raises(ReadAfterWriteError):
        update_population(transaction)


def test_cleanup_trans_city():
    TransCity.collection.delete_every()