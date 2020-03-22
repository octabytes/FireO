---
layout: default
title: DateTime
parent: Fields
nav_order: 7
---

# DateTime Field
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Example Usage

```python
class User(Model):
    created = DateTime()


u = User()
u.created = datetime.datetime.now()
```

## Allowed Attributes

The following attributes supported by DateTime Field.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)
5. [auto](#auto)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required

  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

- ### Validator

  Validate given value of field. This is base attribute that is available in all fields [Read More](/FireO/fields/field#validator)

- ### Auto

Set the auto date if no value is provided

### Example Usage

{: .no_toc }

```python
class User(Model):
    created = DateTime(auto=True)


u = User()
u.save()
print(u.created)
```
