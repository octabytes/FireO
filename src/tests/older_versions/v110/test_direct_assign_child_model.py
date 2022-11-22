from fireo.fields import TextField, NumberField
from fireo.models import Model
from fireo.utils import utils


class DirectParentModel(Model):
    name = TextField()


class DirectChildModel(Model):
    age = NumberField()
    name = TextField(default='default_name')

def test_simple_create_get_direct_child_model():
    p = DirectParentModel.collection.create(name="Direct_Parent_Model")
    c = DirectChildModel.collection.create(parent=p.key, age=26)

    assert utils.get_parent_doc(c.key) == p.key

    child = DirectChildModel.collection.get(c.key)

    assert child.age == 26


def test_create_get_update_direct_child_model():
    p = DirectParentModel.collection.create(name="Direct_Parent_Model")
    c = DirectChildModel.collection.create(parent=p.key, age=26)

    assert c.age == 26
    assert c.name == 'default_name'

    c.name = 'name updated'
    c.update()

    c2 = DirectChildModel.collection.get(c.key)

    assert c2.age == 26
    assert c2.name == 'name updated'

    c2.name = 'another update'
    c2.update()

    c3 = DirectChildModel.collection.get(c2.key)

    assert c3.age == 26
    assert c3.name == 'another update'
