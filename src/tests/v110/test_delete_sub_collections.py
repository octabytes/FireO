from fireo.fields import TextField
from fireo.models import Model


class SubcollectionParent(Model):
    name = TextField()


class SubcollectionChild(Model):
    name = TextField()


def test_delete_sub_collections():
    p = SubcollectionParent.collection.create(name="Parent")
    parent_key = p.key
    c = SubcollectionChild.collection.create(parent=parent_key, name="child")
    child_key = c.key

    child = SubcollectionChild.collection.get(child_key)

    assert child.name == 'child'

    # Delete the parent
    SubcollectionParent.collection.delete(parent_key)

    parent = SubcollectionParent.collection.get(parent_key)

    assert parent is None

    child = SubcollectionChild.collection.get(child_key)

    # Still there is child
    assert child is not None
    assert child.name == 'child'

    # Delete sub collection
    SubcollectionParent.collection.delete(parent_key, child=True)

    child = SubcollectionChild.collection.get(child_key)

    assert child is None