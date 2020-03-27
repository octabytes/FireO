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

For example if you are creating new document and later you want to update it or if you getting document from 
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

### Update NestedModel
{: .no_toc }

But if you are using `NestedModel` then always first `get()` document then `update` otherwise it will create problem 
with `default` values if you set to any field. Because FireO can not know what value you want to add in `updated` document
a new `None` value or the `default` value for this field. So that's why always get `document` first then `update`

### For Example
{: .no_toc }

```python
class Child(Model):
    amount = NumberField(default=7)

class Parent(Model):
    name = TextField()
    child = NestedModel(Child)

m = Parent()
m.name = 'Any Name'
m.child.amount = 10
m.save()

# updating document 
# First get the document then update it without passing key in update method
m = Parent.collectino.get(key)
m.name = 'Updated Name'
m.update()
```

## Update elements in an array
If your document contains an array field, you can use `ListUnion()` and `ListRemove()` to add and remove elements. 
`ListUnion()` adds elements to an array but only elements not already present. `ListRemove()` removes all 
instances of each given element.

```python
city = City.collection.get(city_key)

# Atomically add a new region to the 'regions' list field.
city.regions = fireo.ListUnion(['greater_virginia'])
city.update()

# // Atomically remove a region from the 'regions' List field.
city.regions = fireo.ListRemove(['east_coast'])
city.update()
```

## Increment a numeric value
You can increment or decrement a numeric field value as shown in the following example. 
An increment operation increases or decreases the current value of a field by the given amount. 
If the field does not exist or if the current field value is not a numeric value, the operation 
sets the field to the given value.

```python
city = City.collection.get(city_key)

city.population = fireo.Increment(50)
city.update()
```

## Sub Collection
Sub collection can also update in this same fashion