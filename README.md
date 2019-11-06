<p>
    <h1 align="center">Documentation for FireO</h1>
    <p align="center">
        A modern and simplest convenient ORM package in Python.
        FireO is specifically designed for the Google's Firestore, it's more than just ORM.
        It implements validation, type checking, relational model logic and much more facilities.
    </p>
    <p align="center">
        <strong>
            <a href="https://octabyte.io/FireO">Get Started!</a>
        </strong>
    </p>
    <br><br><br>
</p>

## Installation

```python
pip install fireo
```

## Example Usage

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

## Documentation

Full documentation is available in the [FireO Doc](https://octabyte.io/FireO).

## License

This is official [FireO](https://github.com/octabytes/FireO) Repository. Powered by [OctaByte](https://octabyte.io)
Licensed under [Apache License 2.0](https://github.com/octabytes/FireO/blob/master/LICENSE)
