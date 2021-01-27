---
layout: default
title: Custom Field
parent: Fields
nav_order: 12
---

# Custom Field
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

Create your own custom fields, extend the class from base `Field` or you can extend any existing field also.

## Simple

You can create simplest field just by extending base `Field`

### Example Usage

{: .no_toc }

```python
class WeekDays(Field):
    pass


class User(Model):
    day = WeekDays()

u = User(day=1)
u.save()
```

## Extend DB value

Control how the value of field will be save in Firestore. Override method `db_value()` to change the value.

### Example Usage

{: .no_toc }

```python
class WeekDays(Field):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def db_value(self, val):
        return self.days[val]

u = User(day=0)
u.save()

# This will save "Mon" instead of "0" in Firestore
print(u.day)  # Mon
```

## Extend Field Value

Control how value represent when coming for Firestore. Override method `field_value()` to control this behaviour.

### Example Usage

{: .no_toc }

```python
class WeekDays(Field):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def db_value(self, val):
        return self.days[val]

    def field_value(self, val):
        return self.days.index(val)


u = User(day=0)
u.save()

# This will save "Mon" instead of "0" in Firestore
# But when you get value it will return "0" instead of "Mon"

user = User.collection.get(u.key)
print(user.day)  # 0
```

## Create attributes

[Default](/FireO/fields/field#default), [Required](/FireO/fields/field#required) and [Column Name](/FireO/fields/field#column-name)
attributes are allowed in every field. But you can create more attributes for your field.

### Method to create field attributes

Add filed attribute in the `allowed_attributes` list and then create method for each attribute. Method name must
be start from `attr_` and then the name of the attribute. Method should return the value otherwise `None` value
set for field

_Attribute Method run in the same order as they are specify in `allowed_attributes`_

### Example Usage

```python
class EmailGenerator(Field):
    allowed_attributes = ['prefix', 'domain']

    def attr_prefix(self, attr_val, field_val):
        return attr_val + "." + field_val

    def attr_domain(self, attr_val, field_val):
        return field_val + "@" + attr_val


class User(Model):
    email = EmailGenerator(prefix='prefix', domain='example.com')

u = User()
u.email = 'my_email'
u.save()

# This will save email in Firestore like this "prefix.my_email@example.com"
print(u.email)  #  prefix.my_email@example.com
```
