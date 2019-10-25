---
layout: default
title: Updating Data
parent: Querying Data
nav_order: 2
---

# Updating Data
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

Update document in Firestore collection

## Using Model Instance

Model instance has `update()` method you can update documents using this method

### Example Usage
{: .no_toc }

```python
class User(Model):
    name = TextField()
    age = NumberField()


u = User(name="Azeem", age=26)
u.save()

# Update document
u.name = "Arfan"
u.update()

print(u.name)  # Arfan
print(u.age)  # 26
```

## Using Key
Don't get document just for updating it. This is not efficient way you can pass `key` directly to `update()`
method.

**Don't Do This** *This will take two request one for getting data and second for updating*
```python
u = User.collection.get(user_key)
u.name = "Updated Name"
u.update()

print(u.name)  # Updated Name
print(u.age)  # 26
```

If you don't need to use document value then update the document just passing the `key`

**Do This** *This will take only one request to update document which is efficient*
```python
u = User()
u.name = "Haider"
u.update(user_key)

print(u.name)  # Haider
print(u.age)  # 26
```

### Passing key is not always efficient
{: .no_toc }

For example if you are creating new document and late you want to update it or if you getting document from 
query filter then passing `key` to `update()` is not make it efficient

### For Example
{: .no_toc }

```python
user = User.collection.filter('name', '==', 'Azeem').get()
user.name = 'Update Name'

user.update(user.key)  # This will not make it efficient and this is not recommended way

# Instead of this use update method without passing key
user.update()  # Recommended way
```

## Sub Collection
Sub collection can also update in this same fashion