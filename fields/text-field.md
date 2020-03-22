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
7. [format](#format)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required

  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Column Name

  Set different column name in Firestore instead of field name. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#column-name)

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

- ### Lower case
Firestore is case sensitive if you save name as `Azeem` you can't filter it like `azeem` So it is best 
practice to save data in lower case it help you to search easily. FirO allow to save data in lower case
and search data without case sensitive.

### Example Usage
{: .no_toc }

```python
class User(Model):
    name = TextField(to_lowercase=True)
    age = NumberField()


User.collection.create(name='Azeem', age=26)


# Filter result All three are works and give same result
User.collection.filter('name', '==', 'azeem').get()
User.collection.filter('name', '==', 'Azeem').get()
User.collection.filter('name', '==', 'AzEEm').get()
```

- ### Format
FireO allow to format text in different type, possible format type are `title, upper, lower, capitalize`
format only work when you get data from Firestore. These are not work on saving data. `format=upper` will not 
save the data in uppercase instead it will get data from Firestore and convert it in to uppercase. Simply 
`format` only work with `get` and `fetch` method or after `save` method.

### Example Usage
{: .no_toc }


```python
class User(Model):
    name = TextField(format='upper')

u = User()
u.name = "it's my name"
u.save()

print(u.name) # IT'S MY NAME
```

### Example with get()
{: .no_toc }

```python
class User(Model)
    name = TextField(format='title')

u = User.collection.get(user_key)
print(u.name) # It's My Name
```