import fireo
from fireo.fields import TextField
from fireo.models import Model

"""Tests the creating and updating of firestore create and update timestamps"""
def test_create_and_update_time():
    class Doc(Model):
      doc_id = TextField()
      
      class Meta:
          collection_name = "doc_time"

    doc = Doc(doc_id="test")

    # ensure the create and update are None for new doc
    assert doc.get_firestore_create_time() is None
    assert doc.get_firestore_update_time() is None

    doc.save()

    # ensure the create and update time are set and are equal
    assert doc.get_firestore_create_time() is not None
    assert doc.get_firestore_update_time() is not None
    assert doc.get_firestore_create_time() == doc.get_firestore_update_time()

    create_timestamp_before_update = doc.get_firestore_create_time()
    doc.doc_id = "test 2"

    # ensure modifying a field doesn't change the update time for Firestore
    assert doc.get_firestore_create_time() is not None
    assert doc.get_firestore_update_time() is not None
    assert doc.get_firestore_create_time() == create_timestamp_before_update
    assert doc.get_firestore_create_time() == doc.get_firestore_update_time()

    doc.update()

    # ensure that the update triggers and an update of the update timestamp
    # and that the original create timestamp is still the same
    assert doc.get_firestore_create_time() is not None
    assert doc.get_firestore_update_time() is not None
    assert doc.get_firestore_create_time() == create_timestamp_before_update
    assert doc.get_firestore_create_time() != doc.get_firestore_update_time()

    last_create_time = doc.get_firestore_create_time()
    last_update_time = doc.get_firestore_update_time()
    doc_key = doc.key

    queried_doc = Doc.collection.get(doc_key)

    # ensure the queried doc has the correct create and update timestamp
    assert queried_doc.get_firestore_create_time() is not None
    assert queried_doc.get_firestore_update_time() is not None
    assert queried_doc.get_firestore_create_time() == last_create_time
    assert queried_doc.get_firestore_update_time() == last_update_time



