from fireo.fields import TextField, IDField, BooleanField
from fireo.models import Model
from fireo.managers.errors import EmptyDocument
import pytest


def test_fix_issue_87():
    class CompanyIssue87(Model):
        name = TextField()

    with pytest.raises(EmptyDocument):
        CompanyIssue87.collection.create()

def test_fix_issue_87_save():
    class CompanyIssue87(Model):
        name = TextField()

    c = CompanyIssue87.collection.create(name="some_name")
    assert c.name == "some_name"

def test_fix_issue_87_save_with_default_value():
    class CompanyIssue87(Model):
        name = TextField(default="My Name")

    c = CompanyIssue87()
    c.save()

    assert c.name == "My Name"

def test_fix_issue_87_save_with_bool_value():
    class CompanyIssue87(Model):
        active = BooleanField()

    c = CompanyIssue87()
    c.active = False
    c.save()

    assert c.active == False

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