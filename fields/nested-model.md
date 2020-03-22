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

You can also direct assign the `nested_model` without creating the object.

```python
s = Student()
s.address = 'Student Address'
s.user.name = 'Azeem'  # Here you can assign without creating separate User object
s.save()
```

## Common mistake

Don't save the `NestedModel` otherwise this model will save separately.

**Invalid:** Don't save the `NestedModel`

```python
u = User(name='Nested_Model')
u.save()  # Don't save nested model

s = Student(address="Student_address")
s.user = u
s.save()
```

## Deep Nested Model

There is no limit how how deep you go with nested models. You can create `nested_model` inside another `nested_model`

```python
class Level1(Model):
    name = TextField()


class Level2(Model):
    name = TextField()
    lev1 = NestedModel(Level1)


class Level3(Model):
    name = TextField()
    lev2 = NestedModel(Level2)


l = Level3()
l.name = 'level 1'
l.lev2.name = 'level 2'
l.lev2.lev1.name = 'level 3'
l.save()
```

### Filter Results

{: .no_toc }
You can `filter` models with `nested_models` fields using `dot(.)` notation.

```python
l = Level3.collection.filter('lev2.lev.name', '==', 'level 3').get()
```

## Allowed Attributes

The following attributes supported by Nested Model.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required
  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

But this behave a little different in nested models. If you set `True` then it will check **required** fields inside
nested model if there is any required field and no value is given then it will give error.

### Example

{: .no_toc }

```python
class User(Model):
    name = TextField(required=True)
    age = NumberField()


class Student(Model):
    dept = TextField()
    user = NestedModel(User, required=True)

s = Student()
s.dept = 'Math'
s.user.age = 26
s.save() # ERROR! required field value is missing
```

If you set `False` in nested model then it will not check required field value is provided or not.

```python
class Student(Model):
    dept = TextField()
    user = NestedModel(User, required=False)

s = Student()
s.dept = 'Math'
s.user.age = 26
s.save()  # Successfully saved the result without any error
```

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

- ### Validator
  Validate given value of field. This is base attribute that is available in all fields [Read More](/FireO/fields/field#validator)
