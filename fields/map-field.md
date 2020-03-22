---
layout: default
title: Map Field
parent: Fields
nav_order: 6
---

# Map Field
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

Map field for firestore

## Example Usage

```python
class User(Model):
    marks = MapField()


u = User()
u.marks = {'Math': 70, 'English': 80}
```

## Allowed Attributes

The following attributes supported by Map Field.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required

  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

- ### Validator
  Validate given value of field. This is base attribute that is available in all fields [Read More](/FireO/fields/field#validator)
