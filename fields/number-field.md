---
layout: default
title: Number Field
parent: Fields
nav_order: 3
---

# Number Field
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Example Usage

```python
class User(Model):
    salary = NumberField()


u = User(salary=1000)
u.save()
```

## Allowed Attributes

The following attributes supported by DateTime Field.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)
5. [int_only](#int-only)
6. [float_only](#float-only)
7. [range](#range)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required

  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

- ### Validator

  Validate given value of field. This is base attribute that is available in all fields [Read More](/FireO/fields/field#validator)

- ### Int Only

Allow only integer numbers. Other than integer number it will raise error

### Example Usage

{: .no_toc }

```python
class User(Model):
    salary = NumberField(int_only=True)


u = User(salary=1000)
u.save()
```

- ### Float Only

Allow only float numbers. Other than float number it will raise error

### Example Usage

{: .no_toc }

```python
class User(Model):
    salary = NumberField(float_only=True)


u = User(salary=21.37)
u.save()
```

- ### Range
  Allow number between the range. Syntax `range=(start, stop)`

### Example Usage

{: .no_toc }

```python
class User(Model):
    salary = NumberField(range=(100, 20000))


u = User(salary=1000)
u.save()
```

If you want to allow only max value set the `start` as `None` in this
case there is no minimum limit

```python
class User(Model):
    salary = NumberField(range=(None, 20000))
```

To allow only minimum value set the `stop` as `None` or just put the `start` value only

```python
class User(Model):
    salary = NumberField(range=(100, None))  # Equivalent to range=(100)
```
