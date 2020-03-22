---
layout: default
title: Reference Field
parent: Fields
nav_order: 10
---

# Reference Field
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

A DocumentReference refers to a document location in a Firestore database and can be used to write, read,
or listen to the location. The document at the referenced location may or may not exist.

## Example Usage

```python
class Company(Model):
    name = TextField()


class Employee(Model):
    name = TextField()
    company = ReferenceField(Company)

c = Company(name="Abc_company")
c.save()

e = Employee()
e.name = 'Employee Name'
e.company = c
e.save()
```

## Allowed Attributes

The following attributes supported by Reference Field.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)
5. [auto_load](#auto-load)
6. [on_load](#on-load)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required

  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

- ### Validator

  Validate given value of field. This is base attribute that is available in all fields [Read More](/FireO/fields/field#validator)

- ### Auto Load
  Load reference document automatically, by default it is `True` If you disable the `auto_load` then you can get
  document by `get()` method.

### Example Usage

{: .no_toc }

```python
class Employee(Model):
    name = TextField()
    company = ReferenceField(Company, auto_load=False)


e = Employee.collection.get(emp_key)
print(e.company)  # object of ReferenceDocLoader

# Reference document can be get using get() method
com = e.company.get()
print(com.name)
```

- ### On Load
  Call user specify method when reference document load

### Example Usage

{: .no_toc }

```python
class Employee(Model):
    name = TextField()
    company = ReferenceField(Company, on_load="do_something")

    def do_something(self, company):
        # do something with company document
        print(company.name)
```
