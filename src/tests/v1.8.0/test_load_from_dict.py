from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    class Meta:
        missing_field = 'raise_error'

    value = TextField(column_name='db_value')


def test_load_from_dict_by_name():
    model = MyModel.from_dict({'value': 'value'}, by_column_name=False)

    assert model.value == 'value'


def test_load_from_dict_by_column_name():
    model = MyModel.from_dict({'db_value': 'value'}, by_column_name=True)

    assert model.value == 'value'
