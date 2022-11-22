from fireo.fields import TextField
from fireo.models import Model


class GetAllModel(Model):
    name = TextField()


def test_get_all_documents():
    keys = []
    u = GetAllModel.collection.create(name="Azeem")
    keys.append(u.key)
    u = GetAllModel.collection.create(name="Arfan")
    keys.append(u.key)
    u = GetAllModel.collection.create(name="Haider")
    keys.append(u.key)

    users = GetAllModel.collection.get_all(keys)

    index = 0
    for user in users:
        assert user.name in ['Azeem', 'Arfan', 'Haider']
        index += 1

    assert index == 3