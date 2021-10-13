<p align="right">

![Build Status](https://github.com/octabytes/FireO/actions/workflows/python-package-testing.yml/badge.svg)
<a href="https://badge.fury.io/py/fireo">
    <img src="https://badge.fury.io/py/fireo.svg" alt="PyPI version">
</a>

</p>

<p>
    <h1 align="center"><img src="fireo_logo.png" height="100" alt="FireO Logo"></h1>
    <p align="center">
        A modern and simplest convenient ORM package in Python.
        FireO is specifically designed for the Google's Firestore, it's more than just ORM.
        It implements validation, type checking, relational model logic and much more facilities.
    </p>
    <p align="center">
        <strong>
            <a href="https://octabyte.io/FireO/">Get Started!</a>
        </strong>
    </p>
    <br><br><br>
</p>

## Available in other language

1. FireO is available also in `nodeJS` [FireO nodeJS](https://github.com/octabytes/fireo-nodejs)

## Installation

```python
pip install fireo
```

## Example Usage
```python
from fireo.models import Model
from fireo.fields import TextField

class User(Model):
    name = TextField()


u = User()
u.name = "Azeem Haider"
u.save()

# Get user
user = User.collection.get(u.key)
print(user.name)
```

## Documentation

Full documentation is available in the [FireO Doc](https://octabyte.io/FireO/).

## Contributing

Bug reports and pull requests are welcome. This project is intended to be a safe, welcoming 
space for collaboration, and contributors are expected to adhere to the 
[Contributor Covenant](https://github.com/octabytes/FireO/blob/master/CODE_OF_CONDUCT.md) code of conduct.

1. Fix bug or add new features
2. Write tests for your functionality
3. Mention in [Documentation](https://github.com/octabytes/FireO/tree/gh-pages), what you have done and how others can use it  

To run the tests while developing on this package, you'll have to setup a Google service account and setup credentials with the following command:

`export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"`

See the [Google Cloud documentation](https://cloud.google.com/docs/authentication/getting-started) for more details.

## Code Contributors

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/octabytes/FireO/graphs/contributors"><img src="https://opencollective.com/FireO/contributors.svg?width=890&button=false" /></a>

## License

This is official [FireO](https://github.com/octabytes/FireO) Repository. Powered by [OctaByte](https://octabyte.io)
Licensed under [Apache License 2.0](https://github.com/octabytes/FireO/blob/master/LICENSE)
