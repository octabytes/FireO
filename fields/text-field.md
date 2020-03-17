---
layout: default
title: Text Field
parent: Fields
nav_order: 2
---

# Text Field

{: .no_toc }

## Table of contents

{: .no_toc .text-delta }

1. TOC
   {:toc}

---

## Example Usage

```python
class User(Model):
    name = TextField()


u = User(name="Azeem")
u.save()
```

## Allowed Attributes

The following attributes supported by DateTime Field.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [Lowercase](#lower-case)
5. [validator](#validator)
6. [max_length](#max-length)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required

  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

- ### Lower case

  Firestore is case sensitive FirO allow to save data in lower case and search data without case sensitive. [Read More](/FireO/fields/field#to-lowercase)

- ### Validator

  Validate given value of field. This is base attribute that is available in all fields [Read More](/FireO/fields/field#validator)

- ### Max Length

Maximum length for TextField.

### Example Usage

{: .no_toc }

```python
class User(Model):
    name = TextField(max_length=3)


u = User(name="Azeem")
u.save()

print(u.name)  # Aze
```
