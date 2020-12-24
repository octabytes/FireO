from fireo.fields import TextField, IDField
from fireo.models import Model
from fireo.managers.errors import EmptyDocument
import pytest


def test_fix_issue_87():
    class CompanyIssue87(Model):
        name = TextField()

    with pytest.raises(EmptyDocument):
        CompanyIssue87.collection.create()

def test_fix_issue_87_with_id():
    class CompanyIssue87(Model):
        id = IDField()
        name = TextField()

    with pytest.raises(EmptyDocument):
        CompanyIssue87.collection.create(id="custom-id")

def test_fix_issue_87_with_model_object():
    class CompanyIssue87(Model):
        name = TextField()

    with pytest.raises(EmptyDocument):
        c = CompanyIssue87()
        c.save()

def test_fix_issue_87_with_id_and_object():
    class CompanyIssue87(Model):
        id = IDField()
        name = TextField()

    with pytest.raises(EmptyDocument):
        c = CompanyIssue87()
        c.id = "custom-id"
        c.save()