from fireo.fields import TextField, NestedModel
from fireo.models import Model


def test_simplet_model_convert_into_dict():
    class ConvertModelIntoDict(Model):
        name = TextField()

    c = ConvertModelIntoDict()
    c.name = 'Azeem'
    c.save()

    adict = c.to_dict()

    assert adict['name'] == 'Azeem'


def test_check_after_saving_model_convert_into_dict():
    class ConvertModelIntoDict(Model):
        name = TextField()

    c = ConvertModelIntoDict()
    c.name = 'Azeem'
    c.save()

    c2 = ConvertModelIntoDict.collection.get(c.key)
    adict = c2.to_dict()

    assert adict['name'] == 'Azeem'


def test_nested_model_to_dict():
    class NestedParent(Model):
        name = TextField()

    class ConvertModelIntoDict(Model):
        name = TextField()
        nested_parent = NestedModel(NestedParent, required=True)

    c = ConvertModelIntoDict()
    c.name = 'Azeem'
    c.nested_parent.name = 'nested parent'
    c.save()

    adict = c.to_dict()

    assert adict['name'] == 'Azeem'

    nested_dict = adict['nested_parent']

    assert nested_dict['name'] == 'nested parent'


def test_nested_model_default_args_to_dict():
    class NestedParent(Model):
        name = TextField(default='default parent')

    class ConvertModelIntoDict(Model):
        name = TextField()
        nested_parent = NestedModel(NestedParent, required=True)

    c = ConvertModelIntoDict()
    c.name = 'Azeem'
    c.save()

    adict = c.to_dict()

    assert adict['name'] == 'Azeem'

    nested_dict = adict['nested_parent']

    assert nested_dict['name'] == 'default parent'