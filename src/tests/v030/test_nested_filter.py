from fireo.fields import TextField, NumberField, NestedModel
from fireo.models import Model


class NestedModelFilter(Model):
    name = TextField()


class NestedModelMain(Model):
    age = NumberField()
    user = NestedModel(NestedModelFilter)



n = NestedModelFilter()
n.name = 'Haider'

m = NestedModelMain()
m.age = 26
m.user = n
m.save()

def test_simplet_nested_filter():
    n = NestedModelMain.collection.filter('user.name', '==', 'Haider').get()

    assert n.age == 26
    assert n.user.name == 'Haider'


class NestedModelFilter2(Model):
    name = TextField(column_name='someothername')


class NestedModelMain2(Model):
    age = NumberField()
    user = NestedModel(NestedModelFilter2, column_name='something')


n = NestedModelFilter2()
n.name = 'Haider'

m = NestedModelMain2()
m.age = 26
m.user = n
m.save()


def test_simplet_nested_filter_custom_name():
    n = NestedModelMain.collection.filter('user.name', '==', 'Haider').get()

    assert n.age == 26
    assert n.user.name == 'Haider'