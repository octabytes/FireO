---
layout: default
title: Adding Data
parent: Managing Data
nav_order: 1
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
from fireo import models as mdl


class User(mdl.Model):
    name = mdl.TextField()
    age = mdl.NumberField()


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
from `key` using [utils class](/FireO/utils).and useful when getting, updating or delete data. 
`key` also used for creating sub collections.

### Using From Dict
Model can also create from `dict`

#### Example Usage
{: .no_toc }
```python
model_dict = {'name': 'Azeem', 'age': 26}
u = User.from_dict(model_dict)
u.save()

print(u.id)  # xaIkLAGEjkSON
print(u.key)  # user/xaIkLAGEjkSON
```

### Custom id
Custom id can also be specified by using [IDField](/FireO/fields/id-field)

### Example Usage
{: .no_toc }

```python
from fireo.models import Model
from fireo.fields import IDField, TextField, NumberField


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

If you add [IDField](/FireO/fields/id-field) and not specify any id then id will be stored in this field.

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

## Upsert (Merge fields)
If the document does not exist, it will be created. If the document does exist, its data should be **merged** into the existing document, as follows

### Example Usage
```python
u = User()
u.id = "custom-id"
u.name = "Azeem"
u.save(merge=True)
# OR
u.upsert()

# Both upsert() and save(merge=True) is same thing
```
If you're not sure whether the document exists, pass the option to merge the new data with any existing document to avoid overwriting entire documents.


## Using Manager
Data can be saved by using manger without create model object. Manager return model object after saving data.
`collection` is default manager for models.

### Example Usage
```python
u = User.collection.create(name="Azeem", age=26)

print(u.id)
```

## Preventing get when creating new document
By default when you create new document FireO get this document and return model object.
But you can disable this behavior with `no_return` option

### Example
```python
User.collection.create(no_return=False, name="Azeem", age=27) 
# It will create new User but return None
```

You can also use it with model object `model.save(no_return=False)`

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