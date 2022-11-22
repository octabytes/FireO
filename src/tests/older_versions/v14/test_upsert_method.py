from fireo.fields import TextField, NumberField, IDField
from fireo.models import Model


def test_simple_upsert():
    class SimpleUpsert(Model):
        name = TextField()
        age = NumberField()

    obj = SimpleUpsert()
    obj.name = "Azeem"
    obj.upsert()

    doc = SimpleUpsert.collection.get(obj.key)

    assert doc.name == "Azeem"


def test_update_with_merge():
    class UpdateWithMerge(Model):
        id = IDField()
        name = TextField()
        age = NumberField()

    d1 = UpdateWithMerge()
    d1.id = "update-with-merge-id"
    d1.name = "Azeem"
    d1.save()

    d2 = UpdateWithMerge()
    d2.id = "update-with-merge-id"
    d2.age = 27
    d2.save(merge=True)

    doc = UpdateWithMerge.collection.get(d2.key)

    assert doc.name == "Azeem"
    assert doc.age == 27
