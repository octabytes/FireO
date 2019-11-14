from fireo.fields import TextField, NumberField
from fireo.models import Model
from fireo.utils import utils


class FilterUpdateParent(Model):
    name = TextField()


class FilterUpdateChild(Model):
    name = TextField()
    age = NumberField()


def test_parent_filter_update():
    p = FilterUpdateParent.collection.create(name="Some Name")
    parent_key = p.key

    c = FilterUpdateChild(parent=parent_key)
    c.name = 'Azeem'
    c.age = 26
    c.save()

    c = FilterUpdateChild.collection.parent(parent_key).filter('name','==','Azeem').get()
    assert utils.get_parent_doc(c.key) == parent_key
    print(c.key)
    c.age = 27
    c.update()

    child_key = c.key

    c = FilterUpdateChild.collection.get(child_key)

    assert c.key == child_key
    assert utils.get_parent_doc(c.key) == parent_key
    assert c.name == 'Azeem'
    assert c.age == 27