from fireo.database import db
from fireo.fields import TextField, ReferenceField
from fireo.models import Model


db.local_connection()


class Company(Model):
    name = TextField()


class Employee(Model):
    address = TextField()
    company = ReferenceField(Company)


def test_reference_field():
    c = Company(name="Abc_company")
    c.save()

    e = Employee()
    e.address = 'Employee_address'
    e.company = c
    e.save()

    e2 = Employee.collection.get(e.key)
    assert e2.address == 'Employee_address'
    assert e2.company.name == 'Abc_company'


def test_update_ref_field():
    c = Company(name="Abc_company")
    c.save()

    e = Employee()
    e.address = 'Employee_address'
    e.company = c
    e.save()

    e2 = Employee.collection.get(e.key)
    e2.address = 'updated_address'
    e2.save()

    e3 = Employee.collection.get(e2.key)
    assert e3.address == 'updated_address'
    assert e3.company.name == 'Abc_company'


class Employee2(Model):
    address = TextField()
    company = ReferenceField(Company, auto_load=False)


def test_ref_auto_load():
    c = Company(name="Abc_company")
    c.save()

    e = Employee2()
    e.address = 'Employee_address'
    e.company = c
    e.save()

    e2 = Employee2.collection.get(e.key)

    assert e2.address == 'Employee_address'
    c2 = e2.company.get()
    assert c2.name == 'Abc_company'


class Employee3(Model):
    address = TextField()
    company = ReferenceField(Company, on_load='company_load')

    def company_load(self, c):
        self.c_name = c.name
        assert c.name == 'Abc_company'


def test_ref_on_load():
    c = Company(name="Abc_company")
    c.save()

    e = Employee3()
    e.address = 'Employee_address'
    e.company = c
    e.save()

    e2 = Employee3.collection.get(e.key)
    assert e2.address == 'Employee_address'
    assert e2.company.name == 'Abc_company'
    assert e2.c_name == 'Abc_company'
