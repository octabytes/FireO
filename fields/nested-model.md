---
layout: default
title: Nested Model
parent: Fields
nav_order: 9
---

# Nested Model
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

Model inside another model.

### Example Usage

```python
class User(Model):
    name = TextField()


class Student(Model):
    address = TextField()
    user = NestedModel(User)


u = User(name='Nested_Model')

s = Student(address="Student_address")
s.user = u
s.save()
```

## Common mistake
Don't save the `NestedModel` otherwise this model will save separately and can not be used in other model.

**Invalid:** Don't save the `NestedModel`
```python
u = User(name='Nested_Model')
u.save()  # Don't save nested model

s = Student(address="Student_address")
s.user = u
s.save()
```

## Allowed Attributes

The following attributes supported by Nested Model.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)

- ### Default
Default value for field. This is base attribute that is available in all fields. [Read More](/fields/field/#default)

- ### Required
Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/fields/field/#required)

- ### Column Name
Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/fields/field/#column-name)

- ### Validator
Validate given value of field. This is base attribute that is available in all fields [Read More](/fields/field/#validator)
