from fireo.fields import TextField, ReferenceField
from fireo.models import Model


def test_fix_issue_78():
    class CompanyIssue78(Model):
        name = TextField()

    class EmployeeIssue78(Model):
        name = TextField()
        company = ReferenceField(CompanyIssue78, auto_load=False)

    c = CompanyIssue78(name="Abc_company")
    c.save()

    company_key = c.key

    e = EmployeeIssue78()
    e.name = 'Employee Name'
    e.company = c
    e.save()


    e_l = EmployeeIssue78.collection.filter(company=company_key).fetch()

    count = 0
    for e in e_l:
        count = 1
        assert e.key is not None

    assert count != 0