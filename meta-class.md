---
layout: default
title: Meta Class
nav_order: 6
---

# Meta Class
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

Meta class is used for `Model` configuration. Here are some common configuration for `Model`

1. [Abstract Model](#abstract-model)
2. [Collection Name](#collection-name)
3. [Missing Field](#missing-fields)

## Abstract Model
Abstract model is used to create some common fields into a number of other models.

### Exmaple Usage
{: .no_toc }

```python
class Animal(Model):
    move = TextField()
    eat = TextField()

    class Meta:
        abstract = True


class Bird(Animal):
    name = TextField()


class Fish(Animal):
    name = TextField()


b = Bird()
b.name = 'Sparrow'
b.move = 'Move by Flying'
b.eat = 'Eats bird food'
b.save()


f = Fish()
f.name = 'fish'
f.move = 'Move by swimming'
f.eat = 'Eats sea food'
f.save()
```

## Collection Name
Set collection name in Firestore if no collection name specify then by default Model name will be used for collection,
For example: UserProfile will become user_profile

### Example Usage
{: .no_toc }

```python
class User(Model):
    name = TextField()

    class Meta:
        collection_name = "my_user_collection"
```

## Missing Fields
Manage how fields behave when they are not in `Model` but in Firestore, this is happen when you change model after
adding some records. By default missing field `merge` with the model.
Possible values are **merge, ignore, raise_error**

### Example Usage
{: .no_toc }

```python
class User(Model):
    name = TExtField()
    age = NumberField()

    class Meta:
        missing_field = 'ignore'
```

## Lower case
Firestore is case sensitive if you save name as `Azeem` you can't filter it like `azeem` So it is best 
practice to save data in lower case it help you to search easily. FirO allow to save data in lower case
and search data without case sensitive.

### Example Usage
{: .no_toc }

```python
class User(Model):
    name = TextField()
    age = NumberField()

    class Meta:
        to_lowercase = True

User.collection.create(name='Azeem', age=26)


# Filter result All three are works and give same result
User.collection.filter('name', '==', 'azeem').get()
User.collection.filter('name', '==', 'Azeem').get()
User.collection.filter('name', '==', 'AzEEm').get()
```