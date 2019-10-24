---
layout: default
title: Adding Data
parent: Managing Data
nav_order: 4
---

# Adding Data
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Adding Data
There are two ways to add data in Firestore.

1. [By creating model object](#by-creating-model-object)
2. [Using Manager](#using-manager)

## By creating model object
Create model object and add values to it and `save()` the model. After saving model **model id** and 
**model key** is attached with model object.

### Example Usage

```python
class User(Model):
    name = TextField()
    age = NumberField()


u = User()
u.name = "Azeem"
u.age = 26
u.save()

print(u.id)  # xaIkLAGEjkSON
print(u.key)  # user/xaIkLAGEjkSON 
``` 

### Using Constructor
Values can also be passed in constructor.

#### Example Usage
```python
u = User(name="Azeem", age=26)
u.save()

print(u.id)  # xaIkLAGEjkSON
print(u.key)  # user/xaIkLAGEjkSON
```

`key` contain more information e.g **id, parent collection, parent document** these things can be get 
from `key` using utils class.and useful when getting, updating or delete data. 
`key` also used for creating sub collections.

### Custom id
Custom id can also be specified by using [IDField](/fields/id-field)

### Example Usage
{: .no_toc }

```python
class User(Model):
    user_id = IDField()
    name = TextField()
    age = NumberField()


u = User()
u.user_id = 'custom_doc_id'
u.name = "Azeem"
u.age = 26
u.save()

print(u.user_id)  # custom_doc_id
```

If you add [IDField](/fields/id-field) and not specify any id then id will be stored in this field.

#### Example
{: .no_toc }

```python
u = User()
u.name = "Azeem"
u.age = 26
u.save()

print(u.user_id)  # xaIkLAGEjkSON

# u.id will be None in this case
print(u.id)  # None
```

You can choose any name for id field it can be **id** itself

## Using Manager
Data can be saved by using manger without create model object. Manager return model object after saving data.
`collection` is default manager for models but you can create your own custom managers also.

### Example Usage
```python
u = User.collection.create(name="Azeem", age=26)

print(u.id)
```

## Sub collection
A subcollection is a collection associated with a specific document. In FireO world you can save one model
inside another model parent child relation.

### Example Usage

```python
class Post(Model):
    title = TextField()
    content = TextField()


class Review(Model):
    name = TextFile()
    message = TextFile()


p = Post(title="My First Post", content="Post content")
p.save()

r = Review(parent=p.key)
r.name = "Azeem"
r.message = "Nice post"
r.save()

print(r.key)
```