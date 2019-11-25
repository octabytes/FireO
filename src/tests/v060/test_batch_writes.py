import fireo
from fireo.fields import TextField, NumberField
from fireo.models import Model


class BatchCity(Model):
    name = TextField()
    population = NumberField()


def test_simple_batch_write():
    batch = fireo.batch()

    BatchCity.collection.create(batch=batch, name='CA', population=100)
    c = BatchCity()
    c.name = 'LA'
    c.population = 200
    c.save(batch=batch)

    cities = BatchCity.collection.fetch()
    index = 0
    for city in cities:
        index += 1

    assert index == 0

    batch.commit()

    cities = BatchCity.collection.fetch()
    index = 0
    for city in cities:
        assert city.name in ['CA', 'LA']
        index += 1

    assert index >= 2


def test_batch_update():
    batch = fireo.batch()

    c = BatchCity.collection.create(name='CA', population=300)
    city_key = c.key
    c.population = 400
    c.update(batch=batch)

    city = BatchCity.collection.get(city_key)
    assert city.population == 300

    batch.commit()

    city = BatchCity.collection.get(city_key)
    assert city.population == 400


def test_batch_delete_with_filter():
    batch = fireo.batch()

    BatchCity.collection.create(name='LA', population=100)

    BatchCity.collection.filter('name', '==', 'LA').batch(batch).delete()

    city = BatchCity.collection.filter('name', '==', 'LA').get()
    assert city.name == 'LA'

    batch.commit()

    city = BatchCity.collection.filter('name', '==', 'LA').get()
    assert city is None


def test_batch_delete():
    batch = fireo.batch()

    BatchCity.collection.batch(batch).delete()

    cities = BatchCity.collection.fetch()
    index = 0
    for city in cities:
        index += 1

    assert index >= 2

    batch.commit()

    cities = BatchCity.collection.fetch()
    index = 0
    for city in cities:
        index += 1

    assert index == 0