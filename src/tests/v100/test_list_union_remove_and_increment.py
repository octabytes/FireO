import fireo
from fireo.fields import ListField, NumberField
from fireo.models import Model


class SpecCity(Model):
    states = ListField()
    population = NumberField()


def test_list_union():
    city = SpecCity.collection.create(states=['LA', 'DC'], population=100)
    city.states = fireo.ListUnion(['AB'])
    city.update()

    city = SpecCity.collection.get(city.key)
    assert city.states == ['LA', 'DC', 'AB']


def test_list_remove():
    city = SpecCity.collection.create(states=['LA', 'DC'], population=100)
    city.states = fireo.ListRemove(['DC'])
    city.update()

    city = SpecCity.collection.get(city.key)
    assert city.states == ['LA']


def test_number_increment():
    city = SpecCity.collection.create(states=['LA', 'DC'], population=100)
    city.population = fireo.Increment(50)
    city.update()

    city = SpecCity.collection.get(city.key)
    assert city.population == 150