from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    class Meta:
        collection_name_generator = lambda model_name: f'{model_name}test'

    field = TextField()


def test_collection_name_generator():
    assert MyModel.collection_name == 'MyModeltest'
