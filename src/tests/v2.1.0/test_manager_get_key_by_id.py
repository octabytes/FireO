from fireo.fields import TextField
from fireo.models import Model


class MyModel(Model):
    name = TextField()

    class Meta:
        collection_name = 'my-model'


def test_get_key_by_id():
    assert MyModel.collection.parent('some-parent/doc').get_key_by_id('some-id') == 'some-parent/doc/my-model/some-id'
    assert MyModel.collection.get_key_by_id('some-id') == 'my-model/some-id'
