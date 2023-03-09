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


class NFLevel1(Model):
    name = TextField()


class NFLevel2(Model):
    age = NumberField()
    lev1 = NestedModel(NFLevel1, required=True)


class NFLevel3(Model):
    dept = TextField()
    lev2 = NestedModel(NFLevel2, required=True)


def test_deep_nested_filter_without_column_name():
    l = NFLevel3()
    l.dept = 'Math'
    l.lev2.age = 26
    l.lev2.lev1.name = 'Azeem'
    l.save()

    l = NFLevel3.collection.filter('lev2.lev1.name', '==', 'Azeem').get()

    assert l.dept == 'Math'
    assert l.lev2.age == 26
    assert l.lev2.lev1.name == 'Azeem'


class NFLevel4(Model):
    name = TextField(column_name='lev4name')


class NFLevel5(Model):
    age = NumberField()
    lev4 = NestedModel(NFLevel4, column_name='lev4', required=True)


class NFLevel6(Model):
    dept = TextField()
    lev5 = NestedModel(NFLevel5, column_name='lev5', required=True)


def test_deep_nested_filter_with_column_name():
    l = NFLevel6()
    l.dept = 'Math'
    l.lev5.age = 26
    l.lev5.lev4.name = 'Azeem'
    l.save()

    l = NFLevel6.collection.filter('lev5.lev4.name', '==', 'Azeem').get()

    assert l.dept == 'Math'
    assert l.lev5.age == 26
    assert l.lev5.lev4.name == 'Azeem'