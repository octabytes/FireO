from fireo.fields import TextField, NumberField, NestedModel
from fireo.models import Model


class CreateModelFromDict(Model):
    name = TextField()
    age = NumberField(default=26)


def test_simple_create_from_dict():
    adict = {'name': 'Azeem', 'age': 27}
    c = CreateModelFromDict.from_dict(adict)
    c.save()

    c2 = CreateModelFromDict.collection.get(c.key)
    assert c2.name == 'Azeem'
    assert c2.age == 27


def test_default_paramter_in_create_from_dict():
    adict = {'name': 'Azeem'}
    c = CreateModelFromDict.from_dict(adict)
    c.save()

    c2 = CreateModelFromDict.collection.get(c.key)
    assert c2.name == 'Azeem'
    assert c2.age == 26


def test_create_dict_model_with_nested_model():
    class DictParent(Model):
        name = TextField()

    class CreateModelFromDict2(Model):
        name = TextField()
        nested_parent = NestedModel(DictParent)

    adict = {'name': 'Azeem', 'nested_parent': {'name': 'nested dict model'}}
    c = CreateModelFromDict2.from_dict(adict)
    c.save()

    assert c.name == 'Azeem'
    assert c.nested_parent.name == 'nested dict model'


def test_create_dict_model_with_nested_model_after_saving():
    class DictParent(Model):
        name = TextField()

    class CreateModelFromDict2(Model):
        name = TextField()
        nested_parent = NestedModel(DictParent)

    adict = {'name': 'Azeem', 'nested_parent': {'name': 'nested dict model'}}
    c = CreateModelFromDict2.from_dict(adict)
    c.save()

    c2 = CreateModelFromDict2.collection.get(c.key)

    assert c2.name == 'Azeem'
    assert c2.nested_parent.name == 'nested dict model'
