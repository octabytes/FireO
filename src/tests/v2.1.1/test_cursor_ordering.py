from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField(column_name='my_field')


def test_reverse_order_by():
    cursor = MyModel.collection.order('-field').fetch().cursor

    MyModel.collection.create(field='a')
    MyModel.collection.create(field='b')

    assert [m.field for m in MyModel.collection.cursor(cursor).fetch()] == ['b', 'a']
