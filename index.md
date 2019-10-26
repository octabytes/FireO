---
layout: default
title: Home
nav_order: 1
description: "A modern and simplest convenient ORM package in Python. FireO is specifically designed for 
the Google's Firestore"
permalink: /
---

# FireO is ORM package in Python for the Google's Firestore
{: .fs-9 }

A modern and simplest convenient ORM package in Python. FireO is specifically designed for the Google's Firestore, it's more than just ORM. It implements validation, type checking, relational model logic and much more facilities. 
{: .fs-6 .fw-300 }

[Quickstart](/quick-start){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/ocatbytes/FireO){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Getting started

### Installation

```shell
pip install fireo
```

### Example Usage

```python
class User(Model):
    name = TextField()


u = User()
u.name = "Azeem Haider"
u.save()

# Get user
user = User.collection.get(u.key)
print(user.name)
```

## License

This is official [FireO](https://github.com/octabytes/FireO) Repository. Powered by [OctaByte](https://octabyte.io)
Licensed under GNU General Public License v3.0 [GPL-3.0](https://github.com/octabytes/FireO/blob/master/LICENSE)