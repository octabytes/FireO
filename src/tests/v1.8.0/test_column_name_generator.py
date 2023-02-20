from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    class Meta:
        column_name_generator = str.upper

    field_name = TextField()
    second_field_name = TextField(column_name='TheSecond')


def test_column_name_generator():
    assert MyModel._meta.field_list['field_name'].db_column_name == 'FIELD_NAME'
    assert MyModel._meta.field_list['second_field_name'].db_column_name == 'TheSecond'


