import pytest
from google.cloud import firestore

from fireo.fields import TextField
from fireo.models import Model


# first try with implicit ID model, "unitialized"
# can we use the model to query before using the model to save or get?
def test_issue_168_implicit_id_unitialized():

    class TestIssue168Model(Model):
        name = TextField()

    try:
        TestIssue168Model.collection.filter("name", "==", "test1").fetch()

        assert True == True

    except Exception:
        assert True == False


# use uninitialized model to query data that isn't there
# then see if filter works
def test_issue_168_implicit_id_after_empty_get():

    class TestIssue168Model(Model):
        name = TextField()

    try:
        TestIssue168Model.collection.get("test_issue168_model/id1")
        TestIssue168Model.collection.filter("name", "==", "test1").fetch()

        assert True == True

    except Exception:
        assert True == False


# use uninitialized model to query data that was saved from previous session
# then see if filter works
# not an error case in https://github.com/octabytes/FireO/issues/168
# but adding for test coverage and demo purposes
def test_issue_168_implicit_id_after_get():

    # insert data first
    # this represents data previously written by FireO form another python process
    # hard to simulate without un importing the FireO model in memory, if even possible
    db = firestore.Client()
    doc_ref = db.collection(u'test_issue168_model').document(u'id2')
    doc_ref.set({u'name': u'test2'})

    class TestIssue168Model(Model):
        name = TextField()

    try:
        TestIssue168Model.collection.get("test_issue168_model/id2")
        TestIssue168Model.collection.filter("name", "==", "test1").fetch()

        assert True == True

    except Exception:
        assert True == False
