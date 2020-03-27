from fireo.fields import NumberField
from fireo.models import Model


def test_update_fields_with_default_values():
    class UpdateModelWithDefault(Model):
        amount = NumberField(default=15)


    m = UpdateModelWithDefault(amount=11)
    m.save()

    assert m.amount == 11

    m.update()

    assert m.amount == 11

    m.amount = 13
    m.update()

    assert m.amount == 13