import fireo
from google.cloud.firestore_v1.document import DocumentReference
from fireo.fields import TextField, NumberField
from fireo.models import Model

class City(Model):
    name = TextField()
    population = NumberField()

def test_issue_128_in_document_creation():

    batch = fireo.batch()
    create_ref = City.collection.create(batch=batch, state='NYC', population=500000)

    assert isinstance(create_ref, DocumentReference)

def test_issue_128_in_document_update():

    batch = fireo.batch()
    city = City.collection.create(state='NYC', population=500000)

    city = City()
    city.population = 1000000
    upadte_ref = city.update(key=city.key, batch=batch)

    assert isinstance(upadte_ref, DocumentReference)