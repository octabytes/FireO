from fireo.fields import TextField
from fireo.models import Model


class SubColModel(Model):
    field = TextField()


class MyModel(Model):
    field = TextField()


def test_create_subcollection():
    main = MyModel(field='test').save()
    sub = SubColModel.collection.parent(main.key).create(field='test')

    assert sub.key == f'{main.key}/sub_col_model/{sub.id}'
