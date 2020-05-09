from datetime import datetime
from fireo.fields import DateTime, TextField
from fireo.models import Model


class User(Model):
    name = TextField()
    start = DateTime()


def test_empty_datetime_set():
    now = datetime.now()
    u = User(name='DateTime test',
             start=now)
    u.save()
    value = u.start
    key = u.key
    u.start = None
    u.update()
    u = User.collection.get(key)
    assert(u.start is None)
    u.start = now
    u.update()
    u = User.collection.get(key)
    assert(u.start == value)
