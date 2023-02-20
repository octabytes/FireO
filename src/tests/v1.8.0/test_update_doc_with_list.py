from fireo.fields import ListField, TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField()
    list_field = ListField()


def test_update_doc_with_list():
    m = MyModel(field='value')
    m.list_field = ['list_value']
    m.save()

    m.list_field.append('another_value')
    m.update()

    m = MyModel.collection.get(m.key)
    assert m.list_field == ['list_value', 'another_value']
