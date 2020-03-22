---
layout: default
title: Field
parent: Fields
nav_order: 11
---

# Base Field
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

All fields are extend from base `Field` This field can be used to store any kind of data in Firestore.
This work also like **Dynamic Field** 

### Example Usage

```python
class User(Model):
    name = Field()
    age = Field()


u = User()
u.name = "Azeem"
u.age = 26
u.save()
```

## Allowed Attributes

The following attributes supported by DateTime Field.

1. [default](#default)
2. [required](#required)
3. [column_name](#column-name)
4. [validator](#validator)

- ### Default
Default value for field. This is base attribute that is available in all fields. Set default value for field if no
value is provided

#### Example Usage
{: .no_toc }

```python
class User(Model):
    name = Field(default="Azeem")


u = User()
u.save()

print(u.name)  # Azeem
```

- ### Required
Set `True` if value is required for the field. If no value is provided error raise. 
This is base attribute that is available in all fields

#### Example Usage
{: .no_toc }

```python
class User(Model):
    name = Field(required=True)


u = User()
u.name = "Azeem"
u.save()
```

- ### Column Name

Set different column name in Firestore instead of field name. By default column name is same as the field name
but you can change the column name in Firestore using this attribute. 
This is base attribute that is available in all fields

#### Example Usage
{: .no_toc }

```python
class User(Model):
    name = Field(column_name="full_name")


u = User()
u.name = "Azeem"
u.save()
```

- ### Validator

Validate given value of field. This is base attribute that is available in all fields

#### Example Usage
{: .no_toc }

```python
def check_email(field_val):
    if '@' in field_val:
        return True
    else:
        return False


class User(Model):
    email = Field(validator=check_email)


u = User()
u.email = 'dev@octabyte.io'
u.save()
```

If field not passed the validation then an error will raise. You can also define the custom error message

```python
def check_email(field_val):
    if '@' in field_val:
        return True
    else:
        return (False, 'Email must contain @ sign')
```