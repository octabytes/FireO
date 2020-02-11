from fireo.fields import BooleanField
from fireo.models import Model


def test_update_boolean_false_value():
    class UserBooleanField(Model):
        online = BooleanField()

    u = UserBooleanField()
    u.online = True
    u.save()
    user_key = u.key

    u = UserBooleanField()
    u.online = False
    u.update(user_key)

    assert u.key == user_key
    assert u.online == False
