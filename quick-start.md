---
layout: default
title: Quickstart
nav_order: 3
---

# Quickstart
{: .no_toc }

This quickstart shows you how to set up Cloud Firestore, add, read, update and delete data by using the FireO.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Set up authentication

To run the client library, you must first set up [authentication](/authentication)

## Add data

```python
from fireo.models import Model
from fireo.fields import TextField, NumberField

class User(Model):
    name = TextField()
    age = NumberField()


u = User()
u.name = "Azeem"
u.age = 26
u.save()

print(u.key)
```

## Getting Data

```python
user = User.collection.get(user_key)
print(user.name, user.age)
```

## Update Data

```python
u = User()
u.name = "Arfan"
u.update(user_key)
```

## Delete Data

```python
User.collection.delete(user_key)
```