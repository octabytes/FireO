from fireo import models


class MyModel(models.Model):
    value = models.TextField()
    created_at = models.DateTime(auto=True, required=True)
    updated_at = models.DateTime(auto_update=True, required=True)


def test_required_auto_date():
    m = MyModel()
    m.value = "test"
    m.save()

    assert m.created_at is not None
    assert m.updated_at is not None
    assert m.created_at == m.updated_at
