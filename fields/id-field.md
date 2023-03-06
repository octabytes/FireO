---
layout: default
title: IDField
parent: Fields
nav_order: 1
---

# IDField
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

IDField is special field which is used to specify custom id for documents. If no id specify then id will be
generated automatically.

## Example Usage

```python
from fireo.models import Model
from fireo.fields import IDField

class User(Model):
    user_id = IDField()



u = User()
u.user_id = "custom_doc_id"
u.save()
# After save id will be saved in `user_id`
print(self.user_id)  # custom_doc_id
```

## Allowed Attributes

The following attributes supported by ID Field.

1. [default](#default)
2. [required](#required)
3. [include_in_document](#include-in-document)

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required
  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)

- ### Include in document (v2.0.0)
  Set `True` if you want to include the ID as a field in document. 
  It can be useful if you need to do filters that are not allowed with the document ID in the Firestore.
  Example:
  ```python
  from fireo.models import Model
  from fireo.fields import IDField, TextField
  
  class User(Model):
      id = IDField()
      name = TextField()
  
  user = User(name='John')
  user.save()
  
  # Filter by ID prefix
  # Note: the filtering is done on the document field "id" and not on the document ID.
  id_prefix = 'my-prefix'
  query = User.collection.filter('id', ">=", id_prefix).filter('id', "<", id_prefix + "\ufffd")
  ```
  You still can do filtering by document ID using the `FieldPath.document_id()`:
  ```python
  from google.cloud.firestore_v1.field_path import FieldPath
  
  query = User.collection.filter(FieldPath.document_id(), 'in',  ['some-id', 'some-id-2']) 
  ```