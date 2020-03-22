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
class User(Mode):
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

- ### Default

  Default value for field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#default)

- ### Required
  Set `True` if value is required for the field. This is base attribute that is available in all fields. [Read More](/FireO/fields/field#required)
