from fireo import fields 
from fireo.models import Model

from unittest import mock
 
class TestA(Model): 
    name = fields.TextField(required=True)

class TestB(Model): 
    name = fields.TextField(required=True)
    a_ref = fields.ReferenceField(model_ref=TestA)

    class Meta:
        ignore_none_field = False

def test_reference_field_none_value_filter():
    # Save with null value 
    b = TestB()
    b.name = "Jack"
    b.save()

    # Query for null field value docs
    query = TestB.collection.filter("a_ref", "==", None)
    results = list(query.fetch())
    assert len(results) >= 1
    