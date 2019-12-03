from fireo.fields import TextField, NumberField
from fireo.models import Model


class DirectFilterUser(Model):
    name = TextField()
    age = NumberField()


DirectFilterUser.collection.create(name='Azeem', age=26)


def test_single_direct_filter():
    user = DirectFilterUser.collection.filter(name='Azeem').get()

    assert user.name == 'Azeem'
    assert user.age == 26


def test_multi_direct_filter():
    user = DirectFilterUser.collection.filter(name='Azeem', age=26).get()

    assert user.name == 'Azeem'
    assert user.age == 26


def test_multi_direct_filter2():
    user = DirectFilterUser.collection.filter(name='Azeem').filter(age=26).get()

    assert user.name == 'Azeem'
    assert user.age == 26


def test_combine_direct_filter():
    user = DirectFilterUser.collection.filter(name='Azeem').filter('age', '==', 26).get()

    assert user.name == 'Azeem'
    assert user.age == 26


def test_combine_direct_filter2():
    user = DirectFilterUser.collection.filter(age=26).filter('name', '==', 'Azeem').get()

    assert user.name == 'Azeem'
    assert user.age == 26