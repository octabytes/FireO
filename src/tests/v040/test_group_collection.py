from fireo.fields import TextField
from fireo.models import Model


class City(Model):
    state = TextField()


class Landmark(Model):
    type = TextField()
    name = TextField()


c = City.collection.create(state='SF')
Landmark.collection.parent(c.key).create(type='bridge', name='Golden Gate Bridge')
Landmark.collection.parent(c.key).create(type='museum', name='Legion of Honor')

c = City.collection.create(state='LA')
Landmark.collection.parent(c.key).create(type='park', name='Griffith Park')
Landmark.collection.parent(c.key).create(type='museum', name='The Getty')

c = City.collection.create(state='DC')
Landmark.collection.parent(c.key).create(type='memorial', name='Lincoln Memorial')
Landmark.collection.parent(c.key).create(type='museum', name='National Air and Space Museum')


def test_simple_group_collection():
    landmarks = Landmark.collection.group_fetch()

    index = 0
    for landmark in landmarks:
        assert landmark.type in ['bridge', 'museum', 'park', 'memorial']
        index += 1

    assert index >= 6


def test_update_with_group_collection():
    landmarks = Landmark.collection.filter('name', '==', 'The Getty').group_fetch()
    for landmark in landmarks:
        landmark.name = 'New Updated Name'
        landmark.update()

    landmarks = Landmark.collection.filter('name', '==', 'New Updated Name').group_fetch()
    for landmark in landmarks:
        assert landmark.name == 'New Updated Name'