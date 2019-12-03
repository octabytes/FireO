import fireo
from fireo.fields import TextField
from fireo.models import Model


class DeleteAllModel(Model):
    name = TextField()


def test_simple_delete_all_documents():
    keys = []
    u = DeleteAllModel.collection.create(name="Azeem")
    keys.append(u.key)
    u = DeleteAllModel.collection.create(name="Arfan")
    keys.append(u.key)
    u = DeleteAllModel.collection.create(name="Haider")
    keys.append(u.key)

    users = DeleteAllModel.collection.get_all(keys)

    index = 0
    for user in users:
        assert user.name in ['Azeem', 'Arfan', 'Haider']
        index += 1

    assert index == 3

    DeleteAllModel.collection.delete_all(keys)

    users = DeleteAllModel.collection.get_all(keys)
    for user in users:
        assert user is None


def test_batch_delete_all_documents():
    keys = []
    u = DeleteAllModel.collection.create(name="Azeem1")
    keys.append(u.key)
    u = DeleteAllModel.collection.create(name="Arfan1")
    keys.append(u.key)
    u = DeleteAllModel.collection.create(name="Haider1")
    keys.append(u.key)

    users = DeleteAllModel.collection.get_all(keys)

    for user in users:
        assert user.name in ['Azeem1', 'Arfan1', 'Haider1']

    batch = fireo.batch()
    DeleteAllModel.collection.delete_all(keys, batch)

    for user in users:
        assert user.name in ['Azeem1', 'Arfan1', 'Haider1']

    batch.commit()

    users = DeleteAllModel.collection.get_all(keys)
    for user in users:
        assert user is None