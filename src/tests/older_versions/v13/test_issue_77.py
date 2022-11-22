from fireo.fields import TextField, IDField, DateTime
from fireo.models import Model
from datetime import datetime


def test_fix_issue_77():
    class UserIssue77(Model):
        name = TextField()
        created_on = DateTime(auto=True)

    UserIssue77.collection.create(name="Azeem")
    UserIssue77.collection.create(namae="Haider")
    UserIssue77.collection.create(name="Arfan")

    users = UserIssue77.collection.filter("created_on", "<=", datetime.now()).fetch(2)

    for user in users:
        assert user.key is not None

    c = users.cursor

    assert c is not None

    user_list = UserIssue77.collection.cursor(c).fetch()

    for user in user_list:
        assert user.key is not None
