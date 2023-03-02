from fireo.fields import DateTime, TextField
from fireo.models import Model


class MyModel(Model):
    value = TextField()
    just_at = DateTime()
    created_at = DateTime(auto=True)
    updated_at = DateTime(auto_update=True)


def test_updated_at_is_set_on_create():
    model = MyModel()
    model.value = 'test'
    model.save()

    assert model.just_at is None
    assert model.created_at is not None
    assert model.updated_at is not None
    assert model.created_at == model.updated_at


def test_updated_at_is_updated_on_save():
    model = MyModel()
    model.value = 'test'
    model.save()

    model.value = 'test2'
    model.save()

    assert model.updated_at > model.created_at


def test_updated_at_is_updated_on_update():
    model = MyModel()
    model.value = 'test'
    model.save()

    model.value = 'test2'
    model.update()

    assert model.updated_at > model.created_at


def test_updated_at_is_updated_on_update_with_empty_model():
    model = MyModel()
    model.value = 'test'
    model.save()

    model2 = MyModel()
    model2.update(key=model.key)

    assert model2.updated_at > model.created_at
