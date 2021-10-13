from fireo.fields import TextField, NumberField
from fireo.models import Model

class City(Model):
    name = TextField()
    population = NumberField()

def test_issue_126():
    city = City.collection.create(name='NYC', population=500000, no_return=True)

    assert city == None