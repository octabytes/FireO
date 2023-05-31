from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    field = TextField(column_name='my_field')


def test_to_dict_by_field_name_by_default():
    instance = MyModel()
    instance.field = 'value'

    assert instance.to_dict() == {
        'field': 'value',
        'id': instance.id,
        'key': instance.key,
    }
