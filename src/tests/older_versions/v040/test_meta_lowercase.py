from fireo.fields import TextField, MapField, ListField, Field
from fireo.models import Model


class LowercaseUser(Model):
    txt_name = TextField()
    dict_name = MapField()
    lst_name = ListField()
    base_name = Field()

    class Meta:
        to_lowercase = True


def test_simple_lowercase():
    l = LowercaseUser()
    l.txt_name = 'Azeem'
    l.dict_name = {'name':'Azeem', 'age': 27}
    l.lst_name = ['Azeem', 27]
    l.base_name = 'Azeem'
    l.save()

    l2 = LowercaseUser.collection.get(l.key)

    assert l2.txt_name == 'azeem'
    assert l2.dict_name == {'name':'azeem', 'age': 27}
    assert l2.lst_name == ['azeem', 27]
    assert l2.base_name == 'azeem'


def test_lowercase_with_filter():
    l = LowercaseUser()
    l.txt_name = 'Azeem'
    l.dict_name = {'name': 'Azeem', 'age': 27}
    l.lst_name = ['Azeem', 27]
    l.base_name = 'Azeem'
    l.save()

    l2 = LowercaseUser.collection.filter('txt_name', '==', 'AzEEm').get()

    assert l2.txt_name == 'azeem'
    assert l2.dict_name == {'name': 'azeem', 'age': 27}
    assert l2.lst_name == ['azeem', 27]
    assert l2.base_name == 'azeem'