from fireo.fields import TextField, NumberField
from fireo.models import Model


class DeleteModelUser(Model):
    name = TextField()


class DeleteModelChild(Model):
    age = NumberField()


def test_simple_delete():
    d = DeleteModelUser(name="Name")
    d.save()

    DeleteModelUser.collection.delete(d.key)

    d2 = DeleteModelUser.collection.get(d.key)

    assert d2 is None


def test_multi_delete():
    d = DeleteModelUser(name="Name1")
    d.save()
    d = DeleteModelUser(name="Name2")
    d.save()

    DeleteModelUser.collection.delete_every()

    d2 = DeleteModelUser.collection.fetch()

    assert next(d2, None) is None


def test_parent_delete():
    d = DeleteModelUser(name="Name")
    d.save()
    c = DeleteModelChild(parent=d.key)
    c.age = 26
    c.save()

    DeleteModelChild.collection.delete(c.key)

    c2 = DeleteModelChild.collection.get(c.key)

    assert c2 is None


def test_multi_parent_delete():
    d = DeleteModelUser(name="Name")
    d.save()
    c = DeleteModelChild(parent=d.key)
    c.age = 26
    c.save()
    c = DeleteModelChild(parent=d.key)
    c.age = 27
    c.save()

    DeleteModelChild.collection.parent(d.key).delete_every()

    c2 = DeleteModelChild.collection.parent(d.key).fetch()

    assert next(c2, None) is None