---
layout: default
title: Type Annotation Support
nav_order: 7
description: "FireO supports fields declaration by using type annotation (v2.0.0)"
---

# Type Annotation Support

{: .no_toc }

## Table of contents

{: .no_toc .text-delta }

1. TOC
   {:toc}

---

## TypedModel

`TypedModel` is a model which supports fields declaration by using type annotation.
It is a subclass of `Model` so all the features of `Model` are available in `TypedModel`.

Example:

```python
from fireo.models import TypedModel


class User(TypedModel):
    name: str
    age: int


# User model is ready to use as normal model
u = User()
u.name = "Azeem"
u.age = 26
u.save()
```

## Supported Types

TypedModel supports all the fields which are supported by `Model` including `ListField`, `NestedModelField`
and `MapField`.

Example:

```python
from fireo.typedmodel import TypedModel
from typeing import List, Dict


class Profile(TypedModel):
    address: str
    phone: int


class Comments(TypedModel):
    comment: str
    likes: int


class User(TypedModel):
    name: str
    age: int
    friends_ids: List[str]
    profile: Profile
    comments: List[Comments]
```

## Custom Fields Support

Custom fields support can be added by overriding `annotation_resolver_cls` attribute in Meta:

```python
from fireo.typedmodel import TypedModel
from fireo.fields import TextField
from fireo.fields import AnnotationResolver


class EmailField(TextField):
    pass


class EmailStr(str):
    pass
    

class MyAnnotationResolver(AnnotationResolver):
    resolvers = [
        *AnnotationResolver.resolvers, 
        partial(SimpleFieldResolver, supported_field_type=EmailStr, field_class=EmailField),
    ]



class BaseModel(TypedModel):
    class Meta:
        annotation_resolver_cls = MyAnnotationResolver


class User(BaseModel):
    email: EmailStr


assert User._meta.field_list['email'].__class__ is EmailField
```