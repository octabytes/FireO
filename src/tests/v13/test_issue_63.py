from fireo.fields import TextField, IDField, DateTime
from fireo.models import Model
from datetime import datetime


def test_fix_issue_63():
    class UserIssue63(Model):
        user_id = IDField()
        name = TextField()
        date_added = DateTime()

    u = UserIssue63.collection.create(user_id='1',name='Person Name', date_added=datetime.now())
    
    user = UserIssue63(name='New name')
    user.update(key=u.key)

    assert user.name == 'New name'
    assert user.date_added == u.date_added
