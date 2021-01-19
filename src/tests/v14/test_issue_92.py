from fireo.models import Model
from fireo.fields import TextField, NumberField, IDField
import fireo


def test_issue_92_with_oop():
    class TestIssue92(Model):
        id = IDField()
        name = TextField()
        age = NumberField()

    class TransTest():
        def __init__(self):
            self.model = TestIssue92()

        @fireo.transactional
        def insert_in_transaction(self, transaction, data):
            self.model.from_dict(data).save(transaction=transaction)

    transaction = fireo.transaction()
    data = {'id': 'test-issue-92-id', 'name': 'username', 'age': 27}
    TransTest().insert_in_transaction(transaction, data)

    doc = TestIssue92.collection.get('test_issue92/test-issue-92-id')

    assert doc.name == 'username'
    assert doc.age == 27


def test_issue_92_without_oop():
    class TestIssue92(Model):
        id = IDField()
        name = TextField()
        age = NumberField()

    @fireo.transactional
    def insert_in_transaction(transaction, data):
        TestIssue92.from_dict(data).save(transaction=transaction)

    transaction = fireo.transaction()
    data = {'id': 'test-issue-92-id-2', 'name': 'username', 'age': 27}
    insert_in_transaction(transaction, data)

    doc = TestIssue92.collection.get('test_issue92/test-issue-92-id-2')

    assert doc.name == 'username'
    assert doc.age == 27
