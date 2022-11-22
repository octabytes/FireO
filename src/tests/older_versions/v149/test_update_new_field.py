from fireo.fields import TextField
from fireo.models import Model


class OldModel(Model):
    class Meta:
        collection_name = 'testcolletion'

    first_name = TextField()
    # old Model contains no field 'last_name'


class NewModel(Model):
    class Meta:
        collection_name = 'testcolletion'

    first_name = TextField()
    # now we added 'last_name' field
    last_name = TextField()


def test_update_new_field():
    old_instance = OldModel()
    old_instance.first_name = 'First'
    old_instance.save()

    new_instance: NewModel = NewModel.collection.get(old_instance.key)
    new_instance.last_name = 'Last'
    new_instance.update()

    got_instance = NewModel.collection.get(old_instance.key)
    assert got_instance.last_name == 'Last'
